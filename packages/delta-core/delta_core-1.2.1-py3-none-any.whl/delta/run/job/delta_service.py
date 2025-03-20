import collections
from functools import partial

import ansible_runner
import kubernetes

from delta.run.config import Settings
from delta.run.job import Job, JobService, RunStatus


K8sContainerState = collections.namedtuple("K8sState", ["state", "reason"])


class DeltaJobService(JobService):
    def __init__(self):
        super().__init__()
        self._config = Settings()
        # kubernetes client
        k8s_conf = self.__prepare_kubernetes_config()
        kubernetes.config.load_kube_config_from_dict(k8s_conf)
        self._k8s_cli = kubernetes.client.BatchV1Api()

    def __prepare_ansible_config(self) -> dict:
        return {
            "infra_k8s_namespace": self._config.k8s_namespace,
            "infra_k8s_kubeconfig": {
                "contexts": [
                    {
                        "name": self._config.k8s_context,
                        "cluster": self._config.k8s_cluster_name,
                        "user": self._config.k8s_user_name,
                    }
                ],
                "current_context": self._config.k8s_context,
                "clusters": [
                    {
                        "name": self._config.k8s_cluster_name,
                        "certificate_authority_data":
                            self._config.k8s_cluster_cert_auth,
                        "server": self._config.k8s_cluster_server,
                    }
                ],
                "users": [
                    {
                        "name": self._config.k8s_user_name,
                        "client_certificate_data":
                            self._config.k8s_user_cli_cert,
                        "client_key_data": self._config.k8s_user_cli_key,
                    }
                ]
            },
            "infra_k8s": {
                "registries": [
                    {
                        "name": "gael-harbor",
                        "url": self._config.image_repo_hostname,
                        "login": self._config.image_repo_username,
                        "password": self._config.image_repo_password,
                    }
                ],
                "components": [],
            },
            "resources": {},
            "storage": {
                "data_path": "/s3"
            },
        }

    def __prepare_kubernetes_config(self) -> dict:
        """
        Prepares kubernetes config
        """
        return {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "name": self._config.k8s_cluster_name,
                    "cluster": {
                        "certificate-authority-data":
                            self._config.k8s_cluster_cert_auth,
                        "server": self._config.k8s_cluster_server,
                    },
                }
            ],
            "contexts": [
                {
                    "name": self._config.k8s_context,
                    "context": {
                        "user": self._config.k8s_user_name,
                        "cluster": self._config.k8s_cluster_name,
                    },
                }
            ],
            "current-context": self._config.k8s_context,
            "preferences": {},
            "users": [
                {
                    "name": self._config.k8s_user_name,
                    "user": {
                        "client-certificate-data":
                            self._config.k8s_user_cli_cert,
                        "client-key-data": self._config.k8s_user_cli_key,
                    },
                }
            ],
        }

    @staticmethod
    def __retrieve_container_state_from_pod(
        pod: kubernetes.client.models.V1Pod,
    ) -> K8sContainerState:
        k8s_state = pod.status.container_statuses[0].state
        if k8s_state.running is not None:
            return K8sContainerState("running", None)
        elif k8s_state.terminated is not None:
            return K8sContainerState("terminated", k8s_state.terminated.reason)
        elif k8s_state.waiting is not None:
            return K8sContainerState("waiting", k8s_state.waiting.reason)
        raise ValueError(f"Unknown container state from pod: {pod}")

    @staticmethod
    def __check_container_state(state: K8sContainerState) -> int | None:
        match state:
            case (
                K8sContainerState("running", None)
                | K8sContainerState("terminated", "Terminating")
                | K8sContainerState("waiting", "ContainerCreating")
                | K8sContainerState("waiting", "PodInitializing")
            ):
                return None
            case (
                K8sContainerState("waiting", "ImagePullBackOff")
                | K8sContainerState("waiting", "ErrImagePull")
                | K8sContainerState("waiting", "CrashLoopBackOff")
                | K8sContainerState("waiting", "ImageInspectError")
                | K8sContainerState("waiting", "CreateContainerConfigError")
                | K8sContainerState("waiting", "ErrImageNeverPull")
                | K8sContainerState("waiting", "InvalidImageName")
                | K8sContainerState("terminated", "Error")
                | K8sContainerState("terminated", "OOMKilled")
                | K8sContainerState("terminated", "ContainerCannotRun")
                | K8sContainerState("terminated", "DeadlineExceeded")
                | K8sContainerState("terminated", "ImageGCFailed")
                | K8sContainerState("terminated", "ContainerStatusUnknown")
            ):
                return 1
            case K8sContainerState("terminated", "Completed"):
                return 0
            case _:
                raise ValueError(f"Unknown container state: {state}")

    def my_status_handler(self, job: Job, data, runner_config):
        if data["status"] == "successful":
            self._jobs[job.id] = job
        if data["status"] in ("failed", "timeout", "canceled"):
            self._logger.info(f"Job({job.id}) failed")
            self._logger.error(f"ansible runner error:\n{data}")
            job.status = RunStatus.ERROR

    async def execute_job(self, job: Job, **kwargs):
        # prepare environment variables to execute ansible playbook run_job
        inputs = ";".join(map(lambda x: f"{x.src},{x.dest}", job.inputs))
        outputs = ";".join(map(lambda x: f"{x.src},{x.dest}", job.outputs))
        job_env = self.__prepare_ansible_config()
        job_env["resources"]["inputs"] = inputs
        job_env["resources"]["outputs"] = outputs
        job_env["infra_k8s"]["components"].append({
            "init_container": {
                "type": "s3"
            },
            "job": True,
            "ttl": "100",
            "name": str(job.id),
            "image": f"{self._config.image_repo_hostname}/{job.image.tag}",
            "registry_name": "gael-harbor",
            "cmd": job.command,
            "working_directory": None,
            "environments": [
                {
                    "name": "AWS_BUCKET_NAME",
                    "value": self._config.s3_bucket
                },
                {
                    "name": "AWS_ENDPOINT_URL",
                    "value": self._config.s3_endpoint
                },
                {
                    "name": "AWS_REGION",
                    "value": self._config.s3_region
                },
                {
                    "name": "AWS_ACCESS_KEY_ID",
                    "value": self._config.s3_access_key
                },
                {
                    "name": "AWS_SECRET_ACCESS_KEY",
                    "value": self._config.s3_secret_access_key
                },
            ],
            "ephemeral_volume": {
                "name": "job-volume",
                "size": "5Gi"
            }
        })

        # executing run_job playbook from gael.delta
        try:
            _, r = ansible_runner.run_async(
                private_data_dir="ansibleworkplan",
                extravars=job_env,
                playbook="playbooks/Gael_Delta_run_job_v2.yml",
                suppress_env_files=True,
                quiet=True,
                status_handler=partial(self.my_status_handler, job),
            )
        except Exception as e:
            self._logger.info(f"Job({job.id}) failed: {e}")
            self._logger.error(e)
            job.status = RunStatus.ERROR

    def check_jobs(self):
        for key, job in self._jobs.items():
            self._logger.info(f"Checking running job {key}")
            try:
                k8s_job = self._k8s_cli.read_namespaced_job(
                    name=f"{key}-job",
                    namespace=self._config.k8s_namespace
                )
                status: kubernetes.client.V1JobStatus = k8s_job.status
                if status.succeeded == 1:
                    job.status = RunStatus.SUCCESS
                elif status.failed == 1:
                    job.status = RunStatus.ERROR
            except kubernetes.client.exceptions.ApiException as e:
                self._logger.error(
                    f"Failed to check job status: {key}, reason: {e.reason}"
                )
            except ValueError as e:
                self._logger.error(f"Unknown job status: {e}")
            except Exception:
                self._logger.error("Pod initializing...")

    def shutdown(self):
        pass
