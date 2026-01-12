# Quick Start Guide - NIS-2 Compliance Expert System

This guide will help you get the NIS-2 Compliance Expert System up and running quickly.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- An OpenAI API key (or choose HuggingFace - no key needed)

## Step-by-Step Setup

### 1. Verify Project Structure

Run the validation script to ensure everything is in place:

```bash
python validate_structure.py
```

You should see ✅ indicators for all directories and files.

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- LangChain and related libraries
- OpenAI client
- HuggingFace transformers
- FAISS vector store
- Document loaders (PyPDF, python-docx, etc.)
- Configuration tools (PyYAML)

**Note**: Installation may take 5-10 minutes depending on your connection.

### 4. Set Up API Keys

#### Option A: Using OpenAI (Recommended for best quality)

1. Get an API key from https://platform.openai.com/api-keys
2. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

#### Option B: Using HuggingFace (Free, no API key required)

1. Edit `config.yaml`
2. Change the embeddings provider:
   ```yaml
   embeddings:
     provider: "huggingface"
   ```

### 5. Add Documents

Place your NIS-2 related documents in the `data/documents/` directory:

```bash
# Example documents to add:
data/documents/
├── nis2-directive-en.pdf
├── enisa-guidelines.pdf
├── implementation-guide.pdf
└── national-requirements.txt
```

Supported formats: PDF, TXT, DOCX, HTML

**Where to get NIS-2 documents:**
- Official NIS-2 Directive: https://eur-lex.europa.eu/
- ENISA Guidelines: https://www.enisa.europa.eu/
- National implementation documents from your country's cybersecurity authority

### 6. Run the System

```bash
python main.py
```

**First Run**: The system will:
1. Load your configuration
2. Initialize embeddings
3. Load and process all documents
4. Create FAISS vector index (saved for future runs)
5. Start interactive Q&A session

**Subsequent Runs**: Will load the existing index (much faster)

## Example Usage

Once running, you can ask questions like:

```
Question: What are the main security requirements under NIS-2?

Question: Which organizations must comply with NIS-2?

Question: What are the reporting obligations for security incidents?

Question: What is the timeline for implementing NIS-2 requirements?

Question: What penalties exist for non-compliance?
```

Type `quit`, `exit`, or `q` to exit.

## Configuration Tips

### Adjust Chunk Size

For better context in answers, edit `config.yaml`:

```yaml
document_processing:
  splitter:
    chunk_size: 1500      # Larger chunks = more context
    chunk_overlap: 300    # More overlap = better continuity
```

### Change Number of Retrieved Documents

```yaml
retrieval:
  search_kwargs:
    k: 6  # Retrieve more documents for complex questions
```

### Switch to Conversational Mode

For multi-turn conversations that remember context:

```yaml
retrieval:
  chain_type: "conversational_retrieval"
```

### Adjust LLM Settings

```yaml
retrieval:
  llm:
    model: "gpt-4"           # For better quality (costs more)
    temperature: 0.1         # Lower = more focused, higher = more creative
    max_tokens: 1000        # Longer responses
```

## Troubleshooting

### "No module named 'langchain'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not set"

**Solution**: Either:
1. Set the environment variable: `export OPENAI_API_KEY=your-key`
2. Or switch to HuggingFace in `config.yaml`

### "No documents found"

**Solution**: Add documents to `data/documents/` directory

### "Out of memory" error

**Solution**: Reduce chunk size or process fewer documents:
```yaml
document_processing:
  splitter:
    chunk_size: 500  # Smaller chunks
```

### API rate limit errors

**Solution**: 
1. Reduce batch size when processing documents
2. Add delays between requests
3. Upgrade your OpenAI plan

## Next Steps

1. **Customize Prompts**: Edit `src/chains/retrieval_chain.py` to customize how questions are answered
2. **Add More Documents**: Continuously add relevant compliance documents
3. **Implement Gap Analysis**: Use TODOs in the code as starting points
4. **Create Reports**: Build on the reporting infrastructure
5. **Multi-language**: Add support for other EU languages

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Review code comments for implementation details
- Look for TODO comments for extension points
- Open an issue on GitHub for bugs or questions

## Performance Tips

- **First run is slow**: Document processing and embedding takes time
- **Subsequent runs are fast**: Vector index is cached
- **Large documents**: Split into smaller files for faster processing
- **Better answers**: Use more specific questions
- **Cite sources**: The system returns source documents - check them for accuracy

## Security Notes

- Never commit `.env` file to git (it's in `.gitignore`)
- API keys are sensitive - treat them like passwords
- Audit logs can be enabled in config for compliance tracking
- Review all generated responses for accuracy before using in production

---

**Ready to go?** Run `python main.py` and start exploring NIS-2 compliance!
