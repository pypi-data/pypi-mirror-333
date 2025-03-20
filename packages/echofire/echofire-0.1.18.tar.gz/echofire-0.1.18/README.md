# EchoFire 

**Realistic Voice Agent Testing**  

> Automate end-to-end evaluation of voice agents with human-like audio simulation.  

```mermaid
flowchart LR
    A[Record Session With Voice Agent] --> B[Write Tests w/ LLM Judge + Built-in Functions]
    B --> C{Parallel Test Execution}
    C -->|Multiple Iterations| D1[Run Test 1]
    C -->|Multiple Iterations| D2[Run Test 2]
    C -->|Multiple Iterations| D3[Run Test ...]
    D1 --> E[Share Results & Collaborate]
    D2 --> E
    D3 --> E
    E --> F[Build Datasets for Fine-Tuning]
    F --> G[Improve Models & Prompts]
    G --> A
```

### Why EchoFire?  
- 🚫 **Manual testing sucks**: Listening to every agent response isn't scalable.  
- 🤖 **Synthetic TTS isn't real**: Simulate *actual* human speech patterns, background noise, and ASR edge cases.  
- 🔥 **Test everything**: Validate ASR accuracy, intent logic, and agent responses in one flow.  
- 💻 **Works locally**: Run tests on your machine with a simple CLI - no cloud deployment needed.
- 🔄 **CI/CD ready**: Integrate voice agent testing into your continuous integration pipeline.