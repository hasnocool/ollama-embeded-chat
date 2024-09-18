**README.md**
===============

### Project Title
---------------

Ollama Embedded Chat
=====================

A real-time chat interface that leverages Ollama's AI capabilities and integrates document loading from directories and URLs, caching results in Redis.

### Description
--------------

I built this to create a seamless experience for users who want to engage with AI-driven conversations while also exploring relevant documents. This project combines the power of Ollama's chat models with a custom-built document loader that fetches content from local directories or web URLs, using Selenium for cross-browser compatibility. The fetched documents are then cached in Redis for efficient reuse.

One cool feature is... **live caching**! As soon as you load new documents, they're instantly available within the chat interface without requiring any additional user input.

### Features
------------

*   **Real-time Ollama chat**: Engage with AI-driven conversations directly within this project.
*   **Document loading from directories and URLs**: Fetch relevant content using a custom-built loader that supports multiple sources.
*   **Live caching in Redis**: Store fetched documents for efficient reuse, ensuring that subsequent interactions are blazing fast!
*   **Scalability**: This architecture allows you to add more features and services as needed, without compromising performance.

### Installation
--------------

**Prerequisites**

*   Python 3.8 or higher (`pip` must be available)
*   Redis server (running on `192.168.1.25:6379` by default; adjust according to your setup)

To get started:

```bash
git clone https://github.com/hasnocool/ollama-embeded-chat.git
cd ollama-embeded-chat
pip install -r requirements.txt
```

### Usage
---------

1.  Run the project using `python main.py`
2.  Interact with the chat interface by typing your question or prompt
3.  As you engage in conversations, relevant documents will be loaded and cached automatically

**Tips and Tricks**

*   To add new document sources, modify the `get_urls()` function in `async_chat_client.py`
*   Experiment with different Ollama models by updating the `model` parameter in the `handle_send()` method

### Contributing
--------------

Feel free to fork this project and contribute your ideas or code! I'm all about experimenting with new features and collaborating with fellow developers.

### License
---------

**MIT License**

Copyright (c) 2023 hasnocool

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons who receive copies from you to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

### Tags/Keywords
------------------

*   Ollama Embedded Chat
*   AI-powered chat interface
*   Document loading from directories and URLs
*   Live caching in Redis
*   Real-time conversation
*   Scalable architecture