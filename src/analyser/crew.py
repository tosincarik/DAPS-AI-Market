from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from .real_api import get_real_stock_data, get_real_news_sentiment
from typing import List
import yaml
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Load API keys

@CrewBase
class Analyser:
    """Market Analysis Crew using DAP Protocol"""

    agents_config_path = os.path.join(os.path.dirname(__file__), 'config', 'agents.yaml')
    tasks_config_path = os.path.join(os.path.dirname(__file__), 'config', 'tasks.yaml')

    def __init__(self):
        # Load agents and tasks YAML
        with open(self.agents_config_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open(self.tasks_config_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)

    # --- Agents ---
    @agent
    def chart_analyst(self) -> Agent:
        return Agent(config=self.agents_config['chart_analyst'], verbose=True)

    @agent
    def news_analyst(self) -> Agent:
        return Agent(config=self.agents_config['news_analyst'], verbose=True)

    @agent
    def dap_mediator(self) -> Agent:
        return Agent(config=self.agents_config['dap_mediator'], verbose=True)

    # --- Tasks ---
    @task
    def chart_analysis_task(self) -> Task:
        return Task(config=self.tasks_config['chart_analysis_task'])

    @task
    def news_sentiment_task(self) -> Task:
        return Task(config=self.tasks_config['news_sentiment_task'])

    @task
    def dap_consensus_task(self) -> Task:
        return Task(config=self.tasks_config['dap_consensus_task'])

    # --- Crew ---
    @crew
    def crew(self, inputs: dict = None) -> Crew:
        """Creates the Analyser crew with dynamic inputs (no memoization, dict-safe)"""
        inputs = inputs or {}
        stock_symbol = inputs.get("stock_symbol", "AAPL")
        news_topic = inputs.get("news_topic", f"{stock_symbol} stock")

        # Fetch live API data
        stock_data = get_real_stock_data(stock_symbol)
        news_data = get_real_news_sentiment(news_topic)

        # Context available to all agents/tasks
        context = {
            "stock_symbol": stock_symbol,
            "news_topic": news_topic,
            "stock_data": stock_data,
            "news_data": news_data,
        }

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            context=context,
            verbose=True
        )
