import streamlit as st
from github import Github
from github import UnknownObjectException

# Set up the Streamlit app
st.set_page_config(page_title="GitHub File Search", page_icon=":mag_right:")

# Replace YOUR_ACCESS_TOKEN with your GitHub personal access token
access_token = "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"


# Define a function to get all the repositories that contain a file with the given name
def get_repositories_with_file(filename):
    # Search for the file on GitHub using the PyGitHub library
    g = Github(access_token)
    repositories = g.search_repositories(query=f"filename:{filename}", sort="stars", order="desc")

    # Initialize a list to store the repository information
    repo_info = []

    # Loop through the repositories
    for repo in repositories:
        try:
            # Get all the files in the repository
            contents = repo.get_contents(path=filename)

            # Check if the repository contains a file with the given name
            for content in contents:
                if content.name == filename:
                    repo_info.append({
                        "name": repo.name,
                        "description": repo.description,
                        "url": repo.html_url
                    })
                    break

        except UnknownObjectException as e:
            # Catch the exception if the file is not found in the repository
            st.warning(f"File '{filename}' not found in repository '{repo.full_name}'.")

    # Return the repository information
    return repo_info


# Define the Streamlit app
def app():
    # Set up the user interface
    st.title("GitHub File Search")
    st.write("Enter a file name to search for on GitHub:")
    if filename := st.text_input("File name"):
        # Get the repositories with the file
        repo_info = get_repositories_with_file(filename)

        # Display the repository information
        if len(repo_info) > 0:
            st.success(f"Found {len(repo_info)} repositories with the file '{filename}':")
            for repo in repo_info:
                st.write(f"- **{repo['name']}**: {repo['description']}")
                st.write(f"  URL: [{repo['url']}]({repo['url']})")
        else:
            st.warning(f"No repositories found with the file '{filename}'.")


# Run the Streamlit app
if __name__ == "__main__":
    app()