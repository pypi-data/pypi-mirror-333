"""
OpenAI Node - Interacts with OpenAI API using the official SDK.
Supports all latest model types including GPT-4o, o-series, embeddings, DALL-E, etc.
"""

import logging
import json
import asyncio
import time
import os
from typing import Dict, Any, List, Optional, Union, Tuple

# Import OpenAI SDK
from openai import AsyncOpenAI, OpenAIError

from .base_node import (
    BaseNode, NodeSchema, NodeParameter, NodeParameterType,
    NodeValidationError
)

# Configure logging
logger = logging.getLogger(__name__)

class OpenAIModelType:
    """Categories of OpenAI Models."""
    GPT = "gpt"
    REASONING = "reasoning"
    REALTIME = "realtime"
    AUDIO = "audio"
    DALLE = "dalle"
    TTS = "tts"
    WHISPER = "whisper"
    EMBEDDINGS = "embeddings"
    MODERATION = "moderation"

class OpenAIOperation:
    """Operations available on OpenAI API."""
    CHAT_COMPLETION = "chat_completion"
    EMBEDDING = "embedding"
    IMAGE_GENERATION = "image_generation"
    AUDIO_TRANSCRIPTION = "audio_transcription"
    TEXT_TO_SPEECH = "text_to_speech"
    AUDIO_TRANSLATION = "audio_translation"
    MODERATION = "moderation"
    MODELS_LIST = "models_list"
    FILE_UPLOAD = "file_upload"
    BATCH_CREATE = "batch_create"
    REALTIME_CHAT = "realtime_chat"

class OpenAINode(BaseNode):
    """
    Node for interacting with OpenAI API using the official SDK.
    Provides functionality for all OpenAI service offerings.
    """
    
    # Define operation-parameter mapping as a class attribute
    _operation_parameters = {
        "chat_completion": [
            "operation", "api_key", "org_id", "model_type", "model", 
            "messages", "temperature", "max_tokens", "top_p", 
            "frequency_penalty", "presence_penalty", "stop", "n", 
            "logit_bias", "tools", "tool_choice", "stream",
            "response_format", "seed", "store", "input_image",
            "max_completion_tokens", "reasoning_effort"
        ],
        "embedding": [
            "operation", "api_key", "org_id", "model", "input", "dimensions"
        ],
        "image_generation": [
            "operation", "api_key", "org_id", "model", "prompt", 
            "size", "quality", "style", "image_n"
        ],
        "audio_transcription": [
            "operation", "api_key", "org_id", "model", "audio_file", 
            "audio_language", "audio_response_format"
        ],
        "text_to_speech": [
            "operation", "api_key", "org_id", "model", "tts_text", 
            "tts_voice", "tts_speed", "tts_response_format"
        ],
        "audio_translation": [
            "operation", "api_key", "org_id", "model", "audio_file", 
            "audio_response_format"
        ],
        "moderation": [
            "operation", "api_key", "org_id", "model", "moderation_input"
        ],
        "models_list": [
            "operation", "api_key", "org_id"
        ],
        "file_upload": [
            "operation", "api_key", "org_id", "file_path", "file_purpose"
        ],
        "batch_create": [
            "operation", "api_key", "org_id", "model", "batch_inputs"
        ],
        "realtime_chat": [
            "operation", "api_key", "org_id", "model_type", "model", 
            "messages", "temperature", "max_tokens", "top_p", 
            "frequency_penalty", "presence_penalty", "stop", "n", 
            "logit_bias", "tools", "tool_choice", "stream",
            "response_format", "seed", "store", "input_image",
            "max_completion_tokens", "reasoning_effort"
        ],
    }
    
    def __init__(self, sandbox_timeout: Optional[int] = None):
        super().__init__(sandbox_timeout=sandbox_timeout)
        self.client = None
        
    def get_schema(self) -> NodeSchema:
        """Return the schema definition for the OpenAI node."""
        return NodeSchema(
            node_type="openai",
            version="1.0.0",
            description="Interacts with OpenAI API for various AI operations",
            parameters=[
                # Basic parameters
                NodeParameter(
                    name="operation",
                    type=NodeParameterType.STRING,
                    description="Operation to perform with OpenAI API",
                    required=True,
                    enum=[
                        OpenAIOperation.CHAT_COMPLETION,
                        OpenAIOperation.EMBEDDING,
                        OpenAIOperation.IMAGE_GENERATION,
                        OpenAIOperation.AUDIO_TRANSCRIPTION,
                        OpenAIOperation.TEXT_TO_SPEECH,
                        OpenAIOperation.AUDIO_TRANSLATION,
                        OpenAIOperation.MODERATION,
                        OpenAIOperation.MODELS_LIST,
                        OpenAIOperation.FILE_UPLOAD,
                        OpenAIOperation.BATCH_CREATE,
                        OpenAIOperation.REALTIME_CHAT
                    ]
                ),
                NodeParameter(
                    name="api_key",
                    type=NodeParameterType.STRING,
                    description="OpenAI API key",
                    required=True
                ),
                NodeParameter(
                    name="org_id",
                    type=NodeParameterType.STRING,
                    description="OpenAI organization ID",
                    required=False
                ),
                NodeParameter(
                    name="model_type",
                    type=NodeParameterType.STRING,
                    description="The type of model to use",
                    required=False,
                    enum=[
                        OpenAIModelType.GPT,
                        OpenAIModelType.REASONING,
                        OpenAIModelType.REALTIME,
                        OpenAIModelType.AUDIO,
                        OpenAIModelType.DALLE,
                        OpenAIModelType.TTS,
                        OpenAIModelType.WHISPER,
                        OpenAIModelType.EMBEDDINGS,
                        OpenAIModelType.MODERATION
                    ],
                    default=OpenAIModelType.GPT
                ),
                
                # Model Selection
                NodeParameter(
                    name="model",
                    type=NodeParameterType.STRING,
                    description="OpenAI model to use",
                    required=False,
                    default="gpt-4o"
                ),
                
                NodeParameter(
                    name="max_completion_tokens",
                    type=NodeParameterType.NUMBER,
                    description="Maximum number of tokens to generate (for o-series models)",
                    required=False
                ),
                NodeParameter(
                    name="reasoning_effort",
                    type=NodeParameterType.STRING,
                    description="Level of reasoning effort for o-series models",
                    required=False,
                    enum=["low", "medium", "high", "auto"],
                    default="medium"
                ),

                NodeParameter(
                    name="messages",
                    type=NodeParameterType.ARRAY,
                    description="Messages for chat completion",
                    required=False
                ),
                NodeParameter(
                    name="temperature",
                    type=NodeParameterType.NUMBER,
                    description="Temperature for generation (0-2)",
                    required=False,
                    default=0.7
                ),
                NodeParameter(
                    name="max_tokens",
                    type=NodeParameterType.NUMBER,
                    description="Maximum number of tokens to generate",
                    required=False
                ),
                NodeParameter(
                    name="top_p",
                    type=NodeParameterType.NUMBER,
                    description="Top-p sampling parameter (0-1)",
                    required=False,
                    default=1.0
                ),
                NodeParameter(
                    name="frequency_penalty",
                    type=NodeParameterType.NUMBER,
                    description="Frequency penalty (-2 to 2)",
                    required=False,
                    default=0.0
                ),
                NodeParameter(
                    name="presence_penalty",
                    type=NodeParameterType.NUMBER,
                    description="Presence penalty (-2 to 2)",
                    required=False,
                    default=0.0
                ),
                NodeParameter(
                    name="stop",
                    type=NodeParameterType.ARRAY,
                    description="Sequences where the API will stop generating",
                    required=False
                ),
                NodeParameter(
                    name="n",
                    type=NodeParameterType.NUMBER,
                    description="Number of completions to generate",
                    required=False,
                    default=1
                ),
                NodeParameter(
                    name="logit_bias",
                    type=NodeParameterType.OBJECT,
                    description="Modify the likelihood of specified tokens appearing",
                    required=False
                ),
                NodeParameter(
                    name="tools",
                    type=NodeParameterType.ARRAY,
                    description="List of tools the model may call",
                    required=False
                ),
                NodeParameter(
                    name="tool_choice",
                    type=NodeParameterType.ANY,
                    description="Controls which tool calls the model can make",
                    required=False
                ),
                NodeParameter(
                    name="stream",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether to stream back responses",
                    required=False,
                    default=False
                ),
                NodeParameter(
                    name="response_format",
                    type=NodeParameterType.OBJECT,
                    description="Format to return the response in",
                    required=False
                ),
                NodeParameter(
                    name="seed",
                    type=NodeParameterType.NUMBER,
                    description="Seed for deterministic outputs",
                    required=False
                ),
                NodeParameter(
                    name="store",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether to store the completion for later retrieval",
                    required=False,
                    default=False
                ),
                
                # Image parameters
                NodeParameter(
                    name="input_image",
                    type=NodeParameterType.OBJECT,
                    description="Image input for vision models",
                    required=False
                ),
                
                # Embedding parameters
                NodeParameter(
                    name="input",
                    type=NodeParameterType.ANY,
                    description="Text to get embeddings for (string or array of strings)",
                    required=False
                ),
                NodeParameter(
                    name="dimensions",
                    type=NodeParameterType.NUMBER,
                    description="Number of dimensions for embeddings",
                    required=False
                ),
                
                # DALL-E parameters
                NodeParameter(
                    name="prompt",
                    type=NodeParameterType.STRING,
                    description="Prompt for image generation",
                    required=False
                ),
                NodeParameter(
                    name="size",
                    type=NodeParameterType.STRING,
                    description="Size of generated images",
                    required=False,
                    default="1024x1024",
                    enum=["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
                ),
                NodeParameter(
                    name="quality",
                    type=NodeParameterType.STRING,
                    description="Quality of the generated images",
                    required=False,
                    default="standard",
                    enum=["standard", "hd"]
                ),
                NodeParameter(
                    name="style",
                    type=NodeParameterType.STRING,
                    description="Style of the generated images",
                    required=False,
                    default="vivid",
                    enum=["vivid", "natural"]
                ),
                NodeParameter(
                    name="image_n",
                    type=NodeParameterType.NUMBER,
                    description="Number of images to generate",
                    required=False,
                    default=1
                ),
                
                # Audio transcription parameters
                NodeParameter(
                    name="audio_file",
                    type=NodeParameterType.STRING,
                    description="Path to audio file to transcribe",
                    required=False
                ),
                NodeParameter(
                    name="audio_language",
                    type=NodeParameterType.STRING,
                    description="Language of the audio file (ISO-639-1 format)",
                    required=False
                ),
                NodeParameter(
                    name="audio_response_format",
                    type=NodeParameterType.STRING,
                    description="Format of audio transcription response",
                    required=False,
                    default="json",
                    enum=["json", "text", "srt", "verbose_json", "vtt"]
                ),
                
                # Text-to-speech parameters
                NodeParameter(
                    name="tts_text",
                    type=NodeParameterType.STRING,
                    description="Text to convert to speech",
                    required=False
                ),
                NodeParameter(
                    name="tts_voice",
                    type=NodeParameterType.STRING,
                    description="Voice to use for text-to-speech",
                    required=False,
                    default="alloy",
                    enum=["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
                ),
                NodeParameter(
                    name="tts_speed",
                    type=NodeParameterType.NUMBER,
                    description="Speed of the generated audio",
                    required=False,
                    default=1.0
                ),
                NodeParameter(
                    name="tts_response_format",
                    type=NodeParameterType.STRING,
                    description="Format of the generated audio",
                    required=False,
                    default="mp3",
                    enum=["mp3", "opus", "aac", "flac"]
                ),
                
                # Moderation parameters
                NodeParameter(
                    name="moderation_input",
                    type=NodeParameterType.STRING,
                    description="Text to check for moderation",
                    required=False
                ),
                
                # File upload parameters
                NodeParameter(
                    name="file_path",
                    type=NodeParameterType.STRING,
                    description="Path to file to upload",
                    required=False
                ),
                NodeParameter(
                    name="file_purpose",
                    type=NodeParameterType.STRING,
                    description="Purpose of uploaded file",
                    required=False,
                    default="fine-tune",
                    enum=["fine-tune", "assistants", "vision"]
                ),
                
                # Batch parameters
                NodeParameter(
                    name="batch_inputs",
                    type=NodeParameterType.ARRAY,
                    description="Array of inputs for batch processing",
                    required=False
                ),
            ],
            
            # Define outputs for the node
            outputs={
                "status": NodeParameterType.STRING,
                "result": NodeParameterType.ANY,
                "error": NodeParameterType.STRING,
                "usage": NodeParameterType.OBJECT,
                "model": NodeParameterType.STRING,
                "created_at": NodeParameterType.NUMBER
            },
            
            # Add metadata
            tags=["ai", "openai", "gpt", "reasoning", "embeddings", "dall-e", "whisper", "tts"],
            author="System"
        )
    
    def get_operation_parameters(self, operation: str) -> List[Dict[str, Any]]:
        """
        Get parameters relevant to a specific operation.
        
        Args:
            operation: The operation name (e.g., CHAT_COMPLETION)
            
        Returns:
            List of parameter dictionaries for the operation
        """
        # Remove the prefix if present (e.g., OpenAIOperation.CHAT_COMPLETION -> CHAT_COMPLETION)
        if "." in operation:
            operation = operation.split(".")[-1]
            
        # Convert to lowercase for lookup
        operation_key = operation.lower()
        
        # Get the parameter names for this operation
        param_names = self._operation_parameters.get(operation_key, [])
        
        # Get all parameters from the schema
        all_params = self.get_schema().parameters
        
        # Filter parameters based on the names
        operation_params = []
        for param in all_params:
            if param.name in param_names:
                # Convert to dictionary for the API
                param_dict = {
                    "name": param.name,
                    "type": param.type.value if hasattr(param.type, 'value') else str(param.type),
                    "description": param.description,
                    "required": param.required
                }
                
                # Add optional attributes if present
                if hasattr(param, 'default') and param.default is not None:
                    param_dict["default"] = param.default
                if hasattr(param, 'enum') and param.enum:
                    param_dict["enum"] = param.enum
                
                operation_params.append(param_dict)
        
        return operation_params
    
    def validate_custom(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Custom validation based on the operation type."""
        params = node_data.get("params", {})
        operation = params.get("operation")
        
        if not operation:
            raise NodeValidationError("Operation is required")
            
        # Check for API key
        if not params.get("api_key"):
            raise NodeValidationError("OpenAI API key is required")
            
        # Validate based on operation
        if operation == OpenAIOperation.CHAT_COMPLETION:
            if not params.get("messages"):
                raise NodeValidationError("Messages are required for chat completion")
                
            # Validate messages format
            messages = params.get("messages", [])
            if not isinstance(messages, list) or not messages:
                raise NodeValidationError("Messages must be a non-empty array")
                
            for msg in messages:
                if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                    raise NodeValidationError("Each message must have 'role' and 'content' fields")
                
            # Validate temperature
            temperature = params.get("temperature", 0.7)
            if not isinstance(temperature, (int, float)) or temperature < 0 or temperature > 2:
                raise NodeValidationError("Temperature must be between 0 and 2")
                
        elif operation == OpenAIOperation.EMBEDDING:
            if not params.get("input"):
                raise NodeValidationError("Input text is required for embeddings")
                
        elif operation == OpenAIOperation.IMAGE_GENERATION:
            if not params.get("prompt"):
                raise NodeValidationError("Prompt is required for image generation")
                
            # Validate image count
            image_n = params.get("image_n", 1)
            if not isinstance(image_n, (int, float)) or image_n < 1 or image_n > 10:
                raise NodeValidationError("Number of images must be between 1 and 10")
                
        elif operation == OpenAIOperation.MODERATION:
            if not params.get("moderation_input"):
                raise NodeValidationError("Input text is required for moderation")
                
        elif operation == OpenAIOperation.AUDIO_TRANSCRIPTION:
            if not params.get("audio_file"):
                raise NodeValidationError("Audio file path is required for transcription")
                
            # Check if file exists
            audio_file = params.get("audio_file")
            if not os.path.exists(audio_file):
                raise NodeValidationError(f"Audio file not found: {audio_file}")
                
        elif operation == OpenAIOperation.TEXT_TO_SPEECH:
            if not params.get("tts_text"):
                raise NodeValidationError("Text is required for text-to-speech")
                
        elif operation == OpenAIOperation.FILE_UPLOAD:
            if not params.get("file_path"):
                raise NodeValidationError("File path is required for upload")
                
            # Check if file exists
            file_path = params.get("file_path")
            if not os.path.exists(file_path):
                raise NodeValidationError(f"File not found: {file_path}")
                
        elif operation == OpenAIOperation.BATCH_CREATE:
            if not params.get("batch_inputs"):
                raise NodeValidationError("Batch inputs are required for batch processing")
        
        return {}
    
    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the OpenAI node."""
        try:
            # Validate schema and parameters
            validated_data = self.validate_schema(node_data)
            
            # Get operation type
            operation = validated_data.get("operation")
            
            # Initialize OpenAI client
            api_key = validated_data.get("api_key")
            org_id = validated_data.get("org_id")
            
            # Create OpenAI client with timeout
            self.client = AsyncOpenAI(
                api_key=api_key,
                organization=org_id,
                timeout=60.0  # Set a reasonable timeout
            )
            
            # Execute the appropriate operation
            if operation == OpenAIOperation.CHAT_COMPLETION:
                return await self._operation_chat_completion(validated_data)
            elif operation == OpenAIOperation.EMBEDDING:
                return await self._operation_embedding(validated_data)
            elif operation == OpenAIOperation.IMAGE_GENERATION:
                return await self._operation_image_generation(validated_data)
            elif operation == OpenAIOperation.MODERATION:
                return await self._operation_moderation(validated_data)
            elif operation == OpenAIOperation.MODELS_LIST:
                return await self._operation_models_list(validated_data)
            elif operation == OpenAIOperation.FILE_UPLOAD:
                return await self._operation_file_upload(validated_data)
            elif operation == OpenAIOperation.AUDIO_TRANSCRIPTION:
                return await self._operation_audio_transcription(validated_data)
            elif operation == OpenAIOperation.TEXT_TO_SPEECH:
                return await self._operation_text_to_speech(validated_data)
            elif operation == OpenAIOperation.AUDIO_TRANSLATION:
                return await self._operation_audio_translation(validated_data)
            elif operation == OpenAIOperation.BATCH_CREATE:
                return await self._operation_batch_create(validated_data)
            else:
                error_message = f"Unknown operation: {operation}"
                logger.error(error_message)
                return {
                    "status": "error",
                    "result": None,
                    "error": error_message,
                    "usage": None,
                    "model": None,
                    "created_at": None
                }
                
        except Exception as e:
            error_message = f"Error in OpenAI node: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": None,
                "created_at": None
            }
    
    # -------------------------
    # Operation Methods
    # -------------------------
    
    async def _operation_chat_completion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a chat completion request to the OpenAI API.
        
        Args:
            params: Chat completion parameters
            
        Returns:
            Chat completion results
        """
        # Extract parameters
        messages = params.get("messages", [])
        model = params.get("model", "gpt-4o")
        
        # Add input image to message content if provided
        input_image = params.get("input_image")
        if input_image and isinstance(messages, list) and len(messages) > 0:
            # Find the first user message
            for i, msg in enumerate(messages):
                if msg.get("role") == "user":
                    # If content is a string, convert to list format
                    if isinstance(msg["content"], str):
                        msg["content"] = [{"type": "text", "text": msg["content"]}]
                    # Append image content
                    if isinstance(msg["content"], list):
                        msg["content"].append({
                            "type": "image_url",
                            "image_url": input_image
                        })
                    break
        
        # Check if using an o-series model
        is_o_series = model.startswith("o") and len(model) < 10  # Simple check for o1, o3-mini, etc.
        
        # Build request args differently based on model type
        if is_o_series:
            # O-series models support a limited set of parameters
            request_args = {
                "model": model,
                "messages": messages,
                "stream": params.get("stream", False),
                "store": params.get("store", False)
            }
            
            # Add o-series specific parameters
            reasoning_effort = params.get("reasoning_effort")
            if reasoning_effort is not None:
                request_args["reasoning_effort"] = reasoning_effort
                
            # o-series models use max_completion_tokens instead of max_tokens
            max_completion_tokens = params.get("max_completion_tokens")
            max_tokens = params.get("max_tokens")
            
            if max_completion_tokens is not None:
                request_args["max_completion_tokens"] = max_completion_tokens
            elif max_tokens is not None:
                request_args["max_completion_tokens"] = max_tokens
                
        else:
            # Standard models support the full set of parameters
            request_args = {
                "model": model,
                "messages": messages,
                "temperature": params.get("temperature", 0.7),
                "top_p": params.get("top_p", 1.0),
                "n": params.get("n", 1),
                "frequency_penalty": params.get("frequency_penalty", 0.0),
                "presence_penalty": params.get("presence_penalty", 0.0),
                "stream": params.get("stream", False),
                "store": params.get("store", False)
            }
            
            # Add optional parameters for standard models
            max_tokens = params.get("max_tokens")
            if max_tokens is not None:
                request_args["max_tokens"] = max_tokens
        
        # Common parameters for both model types
        stop = params.get("stop")
        if stop is not None:
            request_args["stop"] = stop
            
        response_format = params.get("response_format")
        if response_format is not None:
            request_args["response_format"] = response_format
            
        # Tools are not supported by o-series models
        if not is_o_series:
            tools = params.get("tools")
            if tools is not None:
                request_args["tools"] = tools
                
            tool_choice = params.get("tool_choice")
            if tool_choice is not None:
                request_args["tool_choice"] = tool_choice
                
            logit_bias = params.get("logit_bias")
            if logit_bias is not None:
                request_args["logit_bias"] = logit_bias
                
            seed = params.get("seed")
            if seed is not None:
                request_args["seed"] = seed
        
        try:
            # Send request
            response = await self.client.chat.completions.create(**request_args)
            
            # Handle streaming responses if enabled
            if params.get("stream", False):
                collected_chunks = []
                collected_messages = []
                
                async for chunk in response:
                    collected_chunks.append(chunk)  # Save the whole chunk
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        collected_messages.append(content)
                
                # Combine and return all messages
                complete_response = {
                    "status": "success",
                    "result": {
                        "choices": [{"message": {"content": "".join(collected_messages)}}]
                    },
                    "usage": collected_chunks[-1].usage.model_dump() if collected_chunks and hasattr(collected_chunks[-1], 'usage') else None,
                    "model": model,
                    "created_at": int(time.time())
                }
                return complete_response
            
            # Process regular response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": result.get("usage"),
                "model": model,
                "created_at": result.get("created")
            }
            
        except OpenAIError as e:
            error_message = f"OpenAI chat completion error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_embedding(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get embeddings from OpenAI API.
        
        Args:
            params: Embedding parameters
            
        Returns:
            Embedding results
        """
        # Extract parameters
        input_text = params.get("input")
        model = params.get("model", "text-embedding-3-small")
        dimensions = params.get("dimensions")
        
        # Build request
        request_args = {
            "model": model,
            "input": input_text
        }
        
        # Add optional parameters
        if dimensions is not None:
            request_args["dimensions"] = dimensions
        
        try:
            # Send request
            response = await self.client.embeddings.create(**request_args)
            
            # Process response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": result.get("usage"),
                "model": model,
                "created_at": result.get("created")
            }
            
        except OpenAIError as e:
            error_message = f"OpenAI embedding error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_image_generation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate images using DALL-E.
        
        Args:
            params: Image generation parameters
            
        Returns:
            Image generation results
        """
        # Extract parameters
        prompt = params.get("prompt")
        size = params.get("size", "1024x1024")
        quality = params.get("quality", "standard")
        style = params.get("style", "vivid")
        n = params.get("image_n", 1)
        model = params.get("model", "dall-e-3")
        
        # Build request
        request_args = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "style": style,
            "n": n
        }
        
        try:
            # Send request
            response = await self.client.images.generate(**request_args)
            
            # Process response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,  # Image generation doesn't provide usage stats
                "model": model,
                "created_at": int(time.time())
            }
            
        except OpenAIError as e:
            error_message = f"OpenAI image generation error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_moderation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check content for policy violations using OpenAI Moderation API.
        
        Args:
            params: Moderation parameters
            
        Returns:
            Moderation results
        """
        # Extract parameters
        input_text = params.get("moderation_input")
        model = params.get("model", "text-moderation-latest")
        
        try:
            # Send request
            response = await self.client.moderations.create(
                input=input_text,
                model=model
            )
            
            # Process response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,  # Moderation doesn't provide usage stats
                "model": model,
                "created_at": int(time.time())
            }
            
        except OpenAIError as e:
            error_message = f"OpenAI moderation error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_models_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List available models.
        
        Args:
            params: Not used
            
        Returns:
            Available models
        """
        try:
            # Send request with a timeout to avoid hanging
            response = await asyncio.wait_for(
                self.client.models.list(),
                timeout=30.0  # 30 second timeout
            )
            
            # Process response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,
                "model": None,
                "created_at": int(time.time())
            }
            
        except asyncio.TimeoutError:
            error_message = "OpenAI models list request timed out"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": None,
                "created_at": None
            }
        except OpenAIError as e:
            error_message = f"OpenAI models list error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": None,
                "created_at": None
            }
    
    async def _operation_file_upload(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload a file to OpenAI API.
        
        Args:
            params: File upload parameters
            
        Returns:
            File upload results
        """
        # Extract parameters
        file_path = params.get("file_path")
        purpose = params.get("file_purpose", "fine-tune")
        
        try:
            # Send request
            with open(file_path, 'rb') as file:
                response = await self.client.files.create(
                    file=file,
                    purpose=purpose
                )
            
            # Process response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,
                "model": None,
                "created_at": result.get("created_at")
            }
            
        except OpenAIError as e:
            error_message = f"OpenAI file upload error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": None,
                "created_at": None
            }
    
    async def _operation_audio_transcription(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transcribe audio to text using OpenAI API.
        
        Args:
            params: Audio transcription parameters
            
        Returns:
            Transcription results
        """
        # Extract parameters
        audio_file = params.get("audio_file")
        language = params.get("audio_language")
        response_format = params.get("audio_response_format", "json")
        model = params.get("model", "whisper-1")
        
        try:
            # Prepare request args
            request_args = {
                "model": model,
                "response_format": response_format
            }
            
            # Add optional parameters
            if language:
                request_args["language"] = language
            
            # Send request
            with open(audio_file, "rb") as file:
                response = await self.client.audio.transcriptions.create(
                    file=file,
                    **request_args
                )
            
            # Process response
            if response_format == "json":
                result = response.model_dump() if hasattr(response, 'model_dump') else {"text": str(response)}
            else:
                # For non-JSON formats, response is just a string
                result = {"text": str(response)}
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,
                "model": model,
                "created_at": int(time.time())
            }
            
        except OpenAIError as e:
            error_message = f"OpenAI audio transcription error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_audio_translation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Translate audio to English text using OpenAI API.
        
        Args:
            params: Audio translation parameters
            
        Returns:
            Translation results
        """
        # Extract parameters
        audio_file = params.get("audio_file")
        response_format = params.get("audio_response_format", "json")
        model = params.get("model", "whisper-1")
        
        try:
            # Prepare request args
            request_args = {
                "model": model,
                "response_format": response_format
            }
            
            # Send request
            with open(audio_file, "rb") as file:
                response = await self.client.audio.translations.create(
                    file=file,
                    **request_args
                )
            
            # Process response
            if response_format == "json":
                result = response.model_dump() if hasattr(response, 'model_dump') else {"text": str(response)}
            else:
                # For non-JSON formats, response is just a string
                result = {"text": str(response)}
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,
                "model": model,
                "created_at": int(time.time())
            }
            
        except OpenAIError as e:
            error_message = f"OpenAI audio translation error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_text_to_speech(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert text to speech using OpenAI API.
        
        Args:
            params: Text-to-speech parameters
            
        Returns:
            Speech generation results
        """
        # Extract parameters
        text = params.get("tts_text")
        voice = params.get("tts_voice", "alloy")
        speed = params.get("tts_speed", 1.0)
        model = params.get("model", "tts-1")
        response_format = params.get("tts_response_format", "mp3")
        
        try:
            # Send request
            response = await self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                speed=speed,
                response_format=response_format
            )
            
            # Get the binary audio data
            audio_data = await response.read()
            
            # Format the response
            return {
                "status": "success",
                "result": {
                    "audio_data": audio_data,
                    "format": response_format,
                    "info": {
                        "text_length": len(text),
                        "voice": voice,
                        "speed": speed
                    }
                },
                "usage": None,
                "model": model,
                "created_at": int(time.time())
            }
            
        except OpenAIError as e:
            error_message = f"OpenAI text-to-speech error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_batch_create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a batch of requests to OpenAI API.
        
        Args:
            params: Batch parameters
            
        Returns:
            Batch creation results
        """
        # Extract parameters
        inputs = params.get("batch_inputs", [])
        model = params.get("model", "gpt-4o")
        
        try:
            # Create batch
            response = await self.client.batches.create(
                model=model, 
                inputs=inputs
            )
            
            # Process response
            result = response.model_dump() if hasattr(response, 'model_dump') else dict(response)
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,
                "model": model,
                "created_at": int(time.time())
            }
            
        except OpenAIError as e:
            error_message = f"OpenAI batch creation error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }

# Register with NodeRegistry
try:
    from base_node import NodeRegistry
    NodeRegistry.register("openai", OpenAINode)
    logger.info("Registered node type: openai")
except Exception as e:
    logger.error(f"Error registering OpenAI node: {str(e)}")