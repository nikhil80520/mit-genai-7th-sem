import asyncio
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.worker import PipelineParams, PipelineWorker
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.services.groq.llm import GroqLLMService
from pipecat.services.groq.stt import GroqSTTService
from pipecat.services.groq.tts import GroqTTSService
from pipecat.transports.local.audio import LocalAudioTransport, LocalAudioTransportParams
from pipecat.workers.runner import WorkerRunner

key = os.getenv("GROQ_API_KEY")

transport = LocalAudioTransport(
    LocalAudioTransportParams(audio_in_enabled=True, audio_out_enabled=True)
)

stt = GroqSTTService(api_key=key)

llm = GroqLLMService(
    api_key=key,
    settings=GroqLLMService.Settings(
        model="openai/gpt-oss-20b",
        system_instruction=(
            "You are a voice assistant. Answer in one or two short sentences. "
            "No lists, no markdown, no emojis."
        ),
        reasoning_effort="low",
    ),
)

tts = GroqTTSService(
    api_key=key,
    settings=GroqTTSService.Settings(voice="autumn"),
)

context = LLMContext()
aggregators = LLMContextAggregatorPair(
    context,
    user_params=LLMUserAggregatorParams(vad_analyzer=SileroVADAnalyzer()),
)

pipeline = Pipeline([
    transport.input(),
    stt,
    aggregators.user(),
    llm,
    tts,
    transport.output(),
    aggregators.assistant(),
])

worker = PipelineWorker(
    pipeline,
    name="assistant",
    params=PipelineParams(enable_metrics=True),
)


async def main():
    runner = WorkerRunner(handle_sigint=False)
    await runner.add_workers(worker)
    run_task = asyncio.create_task(runner.run())
    print("Agent is running. Start talking. Run the next cell to stop it.")
    await runner.cancel()
    try:
        await run_task
    except (Exception, asyncio.CancelledError):
        pass
    print("Stopped.")


if __name__ == "__main__":
    asyncio.run(main())