# -*- coding: utf-8 -*-
from typing import Dict, Any, Optional
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.executor_agent import ExecutorAgent
from agents.prompt_agent import PromptAgent
from agents.merger_agent import MergerAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("SchemaExtractor")

class SchemaExtractorApp:
    def __init__(self, config_file_name: str = None):
        """
        Initialize the Schema Extractor application with its agents.
        
        Args:
            config_file: Optional path to config file. If not provided, uses default config.yaml
        """
        self.executor = ExecutorAgent(config_file=config_file_name)
        self.prompt = PromptAgent(config_file=config_file_name)
        self.merger = MergerAgent(config_file=config_file_name)
        
    def extract_schema(
        self, 
        ttl_file_path: str,
        merge_strategy: str = "comprehensive",
        output_format: str = "text"
    ) -> Dict[str, Any]:
        """
        Extract and analyze schema from a TTL file.
        
        Args:
            ttl_file_path: Path to the TTL file to analyze
            merge_strategy: Strategy for merging results ("comprehensive", "selective", "conflict_resolution")
            output_format: Format of the output ("text" or "json")
            
        Returns:
            Dictionary containing the analysis results
        """
        try:
            # Step 1: Execute TTL file analysis
            logger.info(f"Analyzing TTL file: {ttl_file_path}")
            executor_result = self.executor.process(ttl_file_path=ttl_file_path)
            if executor_result["status"] != "success":
                logger.error((f"Executor agent failed: {executor_result.get('error')}"))
                raise Exception(f"Executor agent failed: {executor_result.get('error')}")
                
            # Step 2: Process schema with prompt agent
            logger.info("Processing schema semantics")
            prompt_result = self.prompt.process(ttl_data=executor_result["execution_result"])
            if prompt_result["status"] != "success":
                logger.error(f"Prompt agent failed: {prompt_result.get('error')}")
                raise Exception(f"Prompt agent failed: {prompt_result.get('error')}")
                
            # Step 3: Merge results
            logger.info(f"Merging results using strategy: {merge_strategy}")
            merged_result = self.merger.process(
                executor_result=executor_result,
                prompt_result=prompt_result,
                merge_strategy=merge_strategy
            )
            if merged_result["status"] != "success":
                logger.error(f"Merger agent failed: {merged_result.get('error')}")
                raise Exception(f"Merger agent failed: {merged_result.get('error')}")
            
            # Format output
            if output_format == "json":
                return {
                    "status": "success",
                    "technical_analysis": executor_result["execution_result"]["data"],
                    "semantic_analysis": prompt_result["response"],
                    "merged_analysis": merged_result["merged_analysis"],
                    "insights": merged_result["insights"]
                }
            else:  # text format
                return {
                    "status": "success",
                    "output": self._format_text_output(
                        executor_result["execution_result"]["data"],
                        prompt_result["response"],
                        merged_result["merged_analysis"],
                        merged_result["insights"]
                    )
                }
                
        except Exception as e:
            error_msg = f"Error analyzing schema: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": error_msg
            }
            
    def _format_text_output(
        self,
        technical: Dict[str, Any],
        semantic: str,
        merged: str,
        insights: str
    ) -> str:
        """Format the analysis results as readable text."""
        output = []
        
        # Technical Analysis
        output.append("=== Technical Analysis ===")
        output.append("\nClasses:")
        for class_uri in technical.get("classes", []):
            output.append(f"- {class_uri}")
            
        output.append("\nProperties:")
        for prop in technical.get("properties", []):
            prop_str = f"- {prop['uri']}"
            if prop['domain']:
                prop_str += f"\n  Domain: {prop['domain']}"
            if prop['range']:
                prop_str += f"\n  Range: {prop['range']}"
            output.append(prop_str)
            
        output.append("\nPrefixes:")
        for prefix, uri in technical.get("prefixes", {}).items():
            output.append(f"- {prefix}: {uri}")
            
        # Semantic Analysis
        output.append("\n=== Semantic Analysis ===")
        output.append(semantic)
        
        # Merged Analysis
        output.append("\n=== Merged Analysis ===")
        output.append(merged)
        
        # Insights
        output.append("\n===  Insights and Recommendations ===")
        output.append(insights)
        
        return "\n".join(output)
