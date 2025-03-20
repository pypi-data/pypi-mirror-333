from galtea.application.services.evaluation_task_service import EvaluationTaskService
from galtea.application.services.metric_type_service import MetricTypeService
from .application.services.product_service import ProductService
from .application.services.test_service import TestService
from .application.services.version_service import VersionService
from .application.services.evaluation_service import EvaluationService
from .infrastructure.clients.http_client import Client
from termcolor import colored

class Galtea:
  def __init__(self, api_key: str):
    self.__client = Client(api_key)
    self.products = ProductService(self.__client)
    self.tests = TestService(self.__client)
    self.versions = VersionService(self.__client)
    self.metrics = MetricTypeService(self.__client)
    self.evaluations = EvaluationService(self.__client)
    self.evaluation_tasks = EvaluationTaskService(self.__client)
  
  def evaluate(self, metrics: list[str] , evaluation_id: str, input: str, actual_output: str, expected_output: str = None, context: str = None):
    """
    Given an evaluation id, create a set of evaluation tasks to evaluate your product based on the metrics provided.
    This function will create a new evaluation task for each metric type provided in the list.
    It will also print the details of each evaluation task created.
    If no evaluation task was created, it will print an error message.
    
    Args:
      metrics (list[str]): List of metric type names.
      evaluation_id (str): ID of the evaluation.
      input (str): Input for the evaluation task.
      actual_output (str): Actual output for the evaluation task.
      expected_output (str, optional): Expected output for the evaluation task.
      context (str, optional): Context for the evaluation task.
      
    Returns:
      list[EvaluationTask]: List of evaluation tasks created.
    """
    evaluation_tasks = self.evaluation_tasks.create(metrics=metrics, evaluation_id=evaluation_id, input=input, actual_output=actual_output, expected_output=expected_output, context=context)
    
    if evaluation_tasks is None or len(evaluation_tasks) == 0:
      print(colored("No evaluation task was created", 'red'))
      return None

    for evaluation_task in evaluation_tasks:      
      if evaluation_task is None:
          print(colored("Error creating evaluation task", 'red'))
          return None
      print(colored("----------------------------------------------------------------", 'green'))
      print(colored(f"→ evaluation_task id: {evaluation_task.id}", 'green'))
      print(colored(f"→ evaluation id: {evaluation_task.evaluation_id}", 'green'))
      print(colored(f"→ metric_id: {evaluation_task.metric_type_id}", 'green'))
      print(colored(f"→ input: {evaluation_task.input}", 'green'))
      print(colored(f"→ actual_output: {evaluation_task.actual_output}", 'green'))
      print(colored(f"→ expected_output: {evaluation_task.expected_output}", 'green'))
      print(colored(f"→ context: {evaluation_task.context}", 'green'))
      print(colored("----------------------------------------------------------------", 'green'))

    return evaluation_tasks
  
