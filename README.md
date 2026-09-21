# Yoummarizer - A Chrome Extension

Yoummarizer is a Chrome extension designed to streamline your YouTube video-watching experience by providing concise summaries of video content. Say goodbye to lengthy videos and get quick insights into the essence of a video.

![Screenshot 2023-10-07 013101](https://github.com/Mohd-Daniyal/Yoummarizer/assets/96229438/6cf3fb53-e641-47f0-af14-a5f082bb3d11)

## Features

- Summarize YouTube videos in real-time.
- Customize the number of tokens for summarization to fit your preferences.
- Save time and gain quick understanding.

## Installation

1. Clone this repository or download the ZIP file.

2. Install the extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`.
   - Enable "Developer mode" in the top right corner.
   - Click "Load unpacked" and select the extension folder.

## Usage

1. Click the Yoummarizer extension icon when watching a YouTube video.

2. Customize the number of tokens (words) for summarization.

3. Enjoy a quick summary of the video's content!

   ![Screenshot 2023-10-07 112839](https://github.com/Mohd-Daniyal/Yoummarizer/assets/96229438/92d627f5-de65-477e-a7f0-faabcc94a4b5)

## OpenAI API Configuration

To use Yoummarizer, you'll need to generate your OpenAI API key and configure it:

1. Visit [OpenAI](https://beta.openai.com/signup/) to sign up for an account or log in.

2. Generate an API key from the OpenAI dashboard.

3. Open the `app.py` file and replace `'YOUR_API_KEY'` with your actual API key.

## Customizing Number of Tokens

You can adjust the number of tokens used for summarization to tailor the length of the summaries according to your preferences. Open the `app.py` file and modify the `max_tokens` argument.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and create a pull request.
