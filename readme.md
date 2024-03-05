# Self-Serve Assets for Embeddable AI using Watson Speech

[Assets/Accelerators for Watson Speech](https://github.com/ibm-ecosystem-engineering/Watson-Speech) (this repo) contains self-serve notebooks and documentation on how to create Speech models using Watson Speech library, how to serve Watson Speech models, and how to make inference requests from custom applications. With an IBM Cloud account a full production sample can be deployed in roughly one hour.

Key Technologies:

- [IBM Watson Speech to Text Library for Embed](https://ibmdocs-test.mybluemix.net/docs/en/watson-libraries?topic=watson-speech-text-library-embed-home) transcribes written text from spoken audio. The service leverages machine learning to combine knowledge of grammar, language structure, and the composition of audio and voice signals to accurately transcribe the human voice. It continuously updates and refines its transcription as it receives more speech audio. The service is ideal for applications that need to extract high-quality speech transcripts for use cases such as call centers, custom care, agent assistance, and similar solutions. You can customize the Watson Text to Speech service to suit your language and application needs. Both services offer HTTP and WebSocket programming interfaces that make them suitable for any application that produces or accepts audio.

- [IBM Watson Text to Speech Library for Embed](https://ibmdocs-test.mybluemix.net/docs/en/watson-libraries?topic=watson-speech-text-library-embed-home) synthesizes natural-sounding speech from written text. The service streams the results back to the client with minimal delay. The service is appropriate for voice-driven and screenless applications, where audio is the preferred method of output. You can customize the Watson Text to Speech service to suit your language and application needs. Both services offer HTTP and WebSocket programming interfaces that make them suitable for any application that produces or accepts audio.

## Outline

- Speech to Text
  - [Watson Speech to Text Analysis Notebook](https://github.com/ibm-ecosystem-engineering/Watson-Speech/blob/main/Speech%20To%20%20Text/Speech%20To%20Text%20Analysis.ipynb)
  - [Deploy a Speech to Text Service on Docker Tutorial](https://github.com/ibm-ecosystem-engineering/Watson-Speech/tree/main/single-container-stt)
- Text to Speech
  - [Watson Text to Speech Tutorial](https://github.com/ibm-ecosystem-engineering/Watson-Speech/blob/main/Text%20To%20Speech/Text-to-Speech-Tutorial.md)
  - [Watson Text to Speech Analysis Notebook](https://github.com/ibm-ecosystem-engineering/Watson-Speech/blob/main/Text%20To%20Speech/Text%20To%20Speech%20Analysis.ipynb)
  - [Deploy a Text to Speech Service with Docker Tutorial](https://github.com/ibm-ecosystem-engineering/Watson-Speech/tree/main/single-container-tts)

## Resources

- IBM Watson Speech Libraries for Embed
  - [Software Announcement](https://www.ibm.com/common/ssi/ShowDoc.wss?docURL=/common/ssi/rep_ca/1/897/ENUS222-291/index.html&lang=en&request_locale=en)
  - [STT Documentation](https://ibmdocs-test.mybluemix.net/docs/en/watson-libraries?topic=watson-speech-text-library-embed-home)
  - [TTS Documentation](https://ibmdocs-test.mybluemix.net/docs/en/watson-libraries?topic=watson-text-speech-library-embed-home)
- IBM Technology Zone assets
  - [Embeddable AI](https://techzone.ibm.com/collection/embedded-ai)
  - [Watson Speech to Text](https://techzone.ibm.com/collection/watson-stt)
  - [Watson Text to Speech](https://techzone.ibm.com/collection/watson-tts)


### Contrbutons By 
Created & Architected By

  Kunal Sawarkar, Chief Data Scientist

Builders

    Michael Spriggs, Principal Architect
    Shivam Solanki, Senior Advisory Data Scientist
    Kevin Huang, Sr. ML-Ops Engineer
    Abhilasha Mangal, Senior Data Scientist
    Himadri Talukder - Senior Software Engineer

Disclaimer

This framework is developed by Build Lab, IBM Ecosystem. Please note that this content is made available to foster Embeddable AI technology adoption and serve ecosystem partners. The content may include systems & methods pending patent with the USPTO and protected under US Patent Laws. SuperKnowa is not a product but a framework built on the top of IBM watsonx along with other products like LLAMA models from Meta & ML Flow from Databricks. Using SuperKnowa implicitly requires agreeing to the Terms and conditions of those products. This framework is made available on an as-is basis to accelerate Enterprise GenAI applications development. In case of any questions, please reach out to kunal@ibm.com.

Copyright @ 2023 IBM Corporation.
