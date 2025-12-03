# Academic Search System Update
## Removed Google Scholar, Enhanced with OpenAI + Offline Caching

**Date:** December 3, 2025  
**Issue:** Google Scholar API (scholarly package) was triggering CAPTCHA errors (HTTP 429 Too Many Requests)

---

## Changes Made

### 1. Removed Google Scholar Integration

**Problem:**
```
INFO:scholarly:Got a captcha request.
HTTP/1.1 429 Too Many Requests
```

**Solution:**
- Removed `scholarly` package from `requirements.txt`
- Removed `scholarly` import from `main.py`
- Deleted `search_google_scholar()` function
- Updated all UI references to remove "Google Scholar" mentions

### 2. Enhanced OpenAI Integration with Offline Caching

**New Workflow:**

```
User Query
    ↓
Check Offline Knowledge Base (512 entries)
    ↓
If confidence ≥ 85% → Return cached answer
    ↓
If not found → Query OpenAI GPT-4
    ↓
Add OpenAI response to offline knowledge base
    ↓
Return answer to user
```

**Benefits:**
- ✅ No more CAPTCHA errors
- ✅ Faster responses from offline cache
- ✅ Growing knowledge base (automatically populated)
- ✅ Works offline after first query
- ✅ More comprehensive answers from GPT-4

### 3. Updated Functions

#### `search_academic(query, use_openai=True)`

**Before:**
- Try OpenAI → Fall back to Google Scholar → Handle errors

**After:**
- Check offline knowledge base first (fast)
- Query OpenAI GPT-4 if not cached
- Automatically cache response for future use
- Return comprehensive academic information

#### `add_to_knowledge_base()`

**New method in `offline_manager.py`:**
```python
def add_to_knowledge_base(self, category: str, question: str, answer: str,
                         source: str = "user", confidence: float = 0.8,
                         difficulty_level: str = "medium", 
                         academic_field: str = "General"):
    """Add entry to knowledge base with extended fields"""
```

Automatically:
- Extracts keywords from question/answer
- Stores in both CSV and SQLite database
- Timestamps all entries
- Tracks confidence scores

### 4. UI Updates

**Changed Text:**
- ❌ "Search Google Scholar & OpenAI assistant"
- ✅ "Search using OpenAI with offline knowledge base"

- ❌ "I can search using Google Scholar and OpenAI"
- ✅ "I can search using OpenAI and our offline knowledge base with 512 university-level entries"

**Menu Items:**
- Removed: "📚 Google Scholar" web link
- Replaced with: "🔍 Academic Resources"

---

## How It Works Now

### First-Time Query

```
User: "Tell me about quantum entanglement"
    ↓
System: Checks offline knowledge base
    ↓
Result: Not found (or low confidence)
    ↓
System: Queries OpenAI GPT-4
    ↓
OpenAI: Returns comprehensive explanation
    ↓
System: Saves to knowledge base (category: AI_Generated, confidence: 0.90)
    ↓
User: Hears detailed response
```

### Subsequent Query (Same Topic)

```
User: "Tell me about quantum entanglement"
    ↓
System: Checks offline knowledge base
    ↓
Result: Found! (confidence: 0.90)
    ↓
System: Returns cached answer immediately
    ↓
User: Hears response (much faster, no API call)
```

---

## Configuration

### OpenAI API Key

**Required:** Set up OpenAI API key in `.env` file:

```bash
OPENAI_API_KEY=your-api-key-here
```

**To get an API key:**
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create new secret key
5. Copy and paste into `.env` file

### Alternative: Use Offline Only

If no OpenAI API key is configured:
- System will only use the offline knowledge base (512 entries)
- No external API calls
- Completely offline operation
- Still provides university-level academic information

---

## Knowledge Base Growth

The system automatically grows over time:

**Initial State:**
- 512 pre-populated university-level entries
- Mathematics, Physics, Chemistry, Biology, Computer Science, etc.

**After Use:**
- Every OpenAI query adds to knowledge base
- Category: "AI_Generated"
- Source: "OpenAI GPT-4"
- Confidence: 0.90

**Example Growth:**

| Week | Entries | Source Distribution |
|------|---------|---------------------|
| 1 | 512 | 100% Pre-populated |
| 2 | 547 | 93% Pre-populated, 7% AI-Generated |
| 4 | 618 | 83% Pre-populated, 17% AI-Generated |
| 8 | 735 | 70% Pre-populated, 30% AI-Generated |

---

## Benefits for Visually Impaired Students

### 1. **Faster Response Times**
- First query: 2-5 seconds (OpenAI API)
- Subsequent queries: < 0.1 seconds (offline cache)
- Better for screen reader users

### 2. **No CAPTCHA Interruptions**
- Google Scholar CAPTCHAs are visual challenges
- Inaccessible for blind students
- Completely eliminated with this update

### 3. **Offline Access**
- Study in areas with poor internet
- No dependency on external services
- Knowledge base stored locally

### 4. **Comprehensive Answers**
- GPT-4 provides detailed, structured responses
- Better for audio consumption
- Includes context, examples, applications

### 5. **Personalized Learning**
- System learns what you search for
- Caches relevant topics
- Faster access to frequently needed information

---

## Error Handling

### OpenAI API Errors

**Scenario:** API key invalid or quota exceeded
```python
error_msg = "OpenAI API error: {error}. Please check your API key and internet connection."
```

**Action:** 
- Display error message
- System continues functioning with offline data
- User can still access 512 pre-populated entries

### No Internet Connection

**Scenario:** Offline environment
- System automatically uses offline knowledge base
- No error messages
- Seamless fallback

### Empty Knowledge Base

**Scenario:** Knowledge base file corrupted
- System auto-initializes with default entries
- Creates new CSV file
- Logs warning for user

---

## Technical Details

### Files Modified

1. **`requirements.txt`**
   - Removed: `scholarly>=1.7.0`

2. **`main.py`**
   - Removed scholarly import
   - Removed `search_google_scholar()` function
   - Enhanced `search_academic()` with offline-first approach
   - Updated UI text (7 locations)

3. **`ai_assistant/offline_manager.py`**
   - Added `add_to_knowledge_base()` method
   - Automatic keyword extraction
   - Extended metadata support

### Dependencies

**Required:**
- `openai>=1.0.0` - For GPT-4 queries
- `pyttsx3>=2.90` - Text-to-speech
- `requests>=2.31.0` - HTTP requests

**Removed:**
- `scholarly>=1.7.0` - Caused CAPTCHA issues

### Data Storage

**CSV Format:** `offline_data/aivi_knowledge_base.csv`
```csv
id,category,question,answer,keywords,source,timestamp,confidence,difficulty_level,academic_field,citation
```

**SQLite Database:** `offline_data/aivi_data.db`
- Full-text search capabilities
- Indexed by keywords
- Access count tracking

---

## Testing

### Test Scenario 1: First-Time Query

```python
# User asks about new topic
query = "explain the Heisenberg uncertainty principle"

# Expected behavior:
1. System checks offline KB → Not found
2. Queries OpenAI GPT-4
3. Receives detailed explanation
4. Saves to KB with confidence=0.90
5. Returns answer to user
6. TTS speaks response
```

### Test Scenario 2: Repeat Query

```python
# User asks same question again
query = "explain the Heisenberg uncertainty principle"

# Expected behavior:
1. System checks offline KB → Found! (confidence 0.90)
2. Returns cached answer immediately
3. No API call
4. Much faster response
5. TTS speaks response
```

### Test Scenario 3: No API Key

```python
# No OPENAI_API_KEY in environment

# Expected behavior:
1. System checks offline KB
2. Uses only pre-populated 512 entries
3. Returns message: "Please set up your OpenAI API key..."
4. System continues working with offline data
```

---

## Future Enhancements

### Planned Features

1. **Confidence Score Adjustment**
   - Track user satisfaction
   - Adjust confidence based on feedback
   - Remove low-quality cached entries

2. **Smart Caching**
   - Identify similar queries
   - Merge related entries
   - Deduplicate knowledge base

3. **Multi-Source Verification**
   - Cross-reference OpenAI with Wikipedia
   - Show source reliability
   - Provide citation information

4. **Advanced Search**
   - Semantic search within knowledge base
   - Related topic suggestions
   - "See also" recommendations

5. **Export/Import**
   - Share knowledge bases between users
   - Import institutional knowledge
   - Export personal study notes

---

## Support

### Common Issues

**Issue:** "OpenAI API error: Authentication failed"
**Solution:** Check `.env` file, ensure API key is valid

**Issue:** Slow responses
**Solution:** Check internet connection, verify API quota

**Issue:** Knowledge base not updating
**Solution:** Check file permissions for `offline_data/` directory

### Contact

For technical support or questions:
- GitHub Issues: https://github.com/TechDreamAfrica/aivi
- Email: support@aivi-edu.org

---

## Summary

✅ **Removed:** Google Scholar integration (CAPTCHA issues)  
✅ **Added:** Offline-first caching system  
✅ **Enhanced:** OpenAI integration with auto-caching  
✅ **Improved:** Accessibility (no visual CAPTCHAs)  
✅ **Faster:** Cached responses < 0.1 seconds  
✅ **Smarter:** Self-improving knowledge base  

**Result:** A more reliable, accessible, and efficient academic search system for visually impaired tertiary students.
