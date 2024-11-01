import asyncio
import argparse

from answer import setup_chains

from comment_retrieval import process_comments

# 1Rc37QkkbGg
def main(video_id):
    # Run the asyncio event loop to process comments and set up QA
    loop = asyncio.get_event_loop()

    video_title, retriever = loop.run_until_complete(process_comments(video_id))
    retrieval_chain = setup_chains(retriever)

    print("\nYou can now start asking questions about the comments.")
    print("Type 'exit' to quit.\n")

    while True:
        # Prompt user for a question
        prompt = input("Enter your question or prompt (or 'exit' to quit): ").strip()
        
        if prompt.lower() == 'exit':
            print("Exiting the Q&A session.")
            break

        for chunk in retrieval_chain.stream({
            "input": prompt,
            "title": video_title,
        }):
            print(chunk, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    # Parse command line argument for video ID
    parser = argparse.ArgumentParser(description="YouTube Comment Q&A Bot")
    parser.add_argument('--video_id', type=str, required=True, help='The ID of the YouTube video')
    args = parser.parse_args()

    # Call the main function with the provided video ID
    main(args.video_id)