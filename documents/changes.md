# VedLinks AI Pipeline Updates

This document outlines the recent critical bug fixes and architectural improvements made to the VedLinks project to ensure fully functional question generation and stability across different environments (including Windows).

## 1. Dynamic Question Generation (RAG Implementation)
**Problem:** Uploaded textbook chapters were returning placeholder "Concept 1, 2, 3" questions because they were not present in the hardcoded `NCERT_KNOWLEDGE` dictionary.
**Fix:**
- Implemented a Retrieval-Augmented Generation (RAG) fallback.
- Newly uploaded PDFs now automatically have their text extracted and cached in the `data/extracted/` directory.
- `QuestionPaperGenerator` now dynamically reads this extracted textbook content.
- Generates real MCQs, fill-in-the-blanks, and short/long answer questions derived directly from the textbook sentences.

## 2. Fuzzy Chapter Matching
**Problem:** Case sensitivity and slight typos prevented the system from finding existing chapters in the `NCERT_KNOWLEDGE` dictionary.
**Fix:**
- Added a 4-level matching system in `get_chapter_knowledge()`.
- Supports exact match, normalized (case-insensitive) match, substring match, and word-overlap matching.
- Example: "control and cordination" now correctly maps to "Control and Coordination".

## 3. Chapter Number Display Bug ("Ch 0")
**Problem:** All uploaded chapters were displaying as "Ch 0" in the UI.
**Fix:** 
- Updated `app.py`'s `get_available_topics()` function to properly extract and include the `chapter_number` field from the structured topic JSON files and topic registry.

## 4. Practice & Concepts Endpoint Fixes
**Problem:** The `/api/practice-questions` and `/api/concepts` endpoints were failing for new chapters.
**Fix:**
- Removed exact `.get()` dictionary lookups.
- Upgraded both endpoints to use the same highly robust fuzzy matching as the main generator.
- Added a secondary fallback ensuring that if no knowledge exists (and AI generation fails), questions are extracted directly from the cached PDF content.

## 5. Windows Training Pipeline Stability
**Problem:** The `train_lora.py` script was crashing on Windows machines due to `bitsandbytes` (4-bit quantization) incompatibilities and dataset configuration errors.
**Fix:**
- **Graceful bnb Fallback**: Added robust `try/except` blocks catching all bitsandbytes errors. If unavailable, training automatically falls back to `float16`.
- **Dynamic Optimizer**: Switches from `paged_adamw_32bit` (requires bitsandbytes) to standard PyTorch `adamw_torch` when necessary.
- **CPU Offloading**: Disables `gradient_checkpointing` when running on CPU to prevent locking.
- **Dataloader Fix**: Sets `num_workers=0` specifically for Windows to prevent multiprocessing locking.
- **TRL Version Immunity**: Configured `SFTConfig` dynamically to check which parameters (`max_length` vs `max_seq_length`) the user's specific `trl` version supports, preventing keyword argument crashes.
