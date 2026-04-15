import streamlit as st
import requests
from bs4 import BeautifulSoup

# -------------------------------
# Function: Scrape Website Data
# -------------------------------
def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title = soup.title.string.strip() if soup.title else "No title found"

        # Meta Description
        meta_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else "No meta description found"

        # Content
        content = soup.get_text()
        word_count = len(content.split())

        # Images
        images = soup.find_all("img")

        return title, meta_desc, content, images, word_count

    except Exception as e:
        return None, None, None, None, str(e)


# -------------------------------
# Function: Analyze SEO
# -------------------------------
def analyze_seo(title, meta_desc, word_count, images):
    issues = []

    # Title Check
    if len(title) < 50:
        issues.append("Title is too short (Recommended: 50–60 characters)")
    elif len(title) > 60:
        issues.append("Title is too long (Recommended: 50–60 characters)")

    # Meta Description Check
    if "No meta description" in meta_desc:
        issues.append("Meta description is missing")

    # Content Length Check
    if word_count < 300:
        issues.append("Content is too short (Recommended: 800+ words)")

    # Image ALT Check
    missing_alt = sum(1 for img in images if not img.get("alt"))
    if missing_alt > 0:
        issues.append(f"{missing_alt} images are missing ALT tags")

    return issues


# -------------------------------
# Function: Generate Suggestions
# -------------------------------
def generate_suggestions(issues):
    suggestions = []

    for issue in issues:
        if "Title" in issue:
            suggestions.append("Optimize title to 50–60 characters and include primary keyword")
        if "Meta" in issue:
            suggestions.append("Add a compelling meta description (150–160 characters)")
        if "Content" in issue:
            suggestions.append("Increase content length and add valuable information")
        if "ALT" in issue:
            suggestions.append("Add descriptive ALT text to all images")

    return list(set(suggestions))


# -------------------------------
# Function: Calculate SEO Score
# -------------------------------
def calculate_score(issues):
    score = 100 - (len(issues) * 10)
    return max(score, 0)


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="SEO Doctor AI", layout="centered")

st.title("🔍 SEO Doctor AI")
st.write("Analyze your website and get SEO improvement suggestions")

url = st.text_input("Enter Website URL (with https://)")

if st.button("Analyze Website"):

    if not url.startswith("http"):
        st.error("Please enter a valid URL starting with http or https")
    else:
        with st.spinner("Analyzing website..."):

            title, meta_desc, content, images, word_count = scrape_website(url)

            if title is None:
                st.error(f"Error fetching website: {word_count}")
            else:
                issues = analyze_seo(title, meta_desc, word_count, images)
                suggestions = generate_suggestions(issues)
                score = calculate_score(issues)

                # Display Results
                st.subheader("📊 SEO Score")
                st.success(f"{score} / 100")

                st.subheader("📄 Website Overview")
                st.write(f"**Title:** {title}")
                st.write(f"**Meta Description:** {meta_desc}")
                st.write(f"**Word Count:** {word_count}")
                st.write(f"**Total Images:** {len(images)}")

                st.subheader("❌ Issues Found")
                if issues:
                    for issue in issues:
                        st.write(f"- {issue}")
                else:
                    st.write("No major SEO issues found 🎉")

                st.subheader("✅ Recommendations")
                if suggestions:
                    for suggestion in suggestions:
                        st.write(f"- {suggestion}")
                else:
                    st.write("Your website is well optimized 👍")
