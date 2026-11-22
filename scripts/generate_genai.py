#!/usr/bin/env python3
"""Generate perfected Generative AI architecture diagrams: Transformer & Advanced RAG."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_transformer():
    d = DiagramBuilder()
    d.add_header(
        "Autoregressive LLM Architecture: Modern Transformer Decoder Block",
        "RoPE (Rotary Position), Grouped-Query Attention (GQA), KV Cache, and SwiGLU Feed-Forward",
        x=40, y=20, w=1220, h=65
    )

    # Left Container: Decoder Block Stack (x=40..730, w=690, h=605)
    d.add_container(40, 105, 690, 605, label="Transformer Decoder Layer (Nx Layers, e.g. 32x in LLaMA-3)", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5", badge_w=460)

    # Column 1 (Left Stack): Execution Hierarchy (x=60..360, w=300)
    d.add_box(60, 150, 300, 48, "Input Tokens [x_1, x_2 ... x_t]", "BPE Tokenizer IDs (Vocabulary: 128k)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(210, 198, 210, 222, stroke="#1971c2")

    d.add_box(60, 222, 300, 48, "Token Embeddings + RoPE", "Rotary Position Embeddings rotate Q, K", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(210, 270, 210, 292, stroke="#1971c2")

    d.add_box(60, 292, 300, 40, "RMSNorm 1 (Pre-Attention)", "Root-mean-square normalization (Pre-Norm)", bg="#f1f3f5", stroke="#495057", text_color="#212529", font_size=11)
    d.add_arrow(210, 332, 210, 352, stroke="#495057")

    d.add_box(60, 352, 300, 56, "Grouped-Query Attention (GQA)", "Q: 32 heads, K/V: 8 heads (saves 75% VRAM)\nSoftmax((Q K^T / √d_k) + M) * V [Causal]", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)
    d.add_arrow(210, 408, 210, 430, stroke="#9c36b5")

    d.add_box(60, 430, 300, 40, "Residual Add 1 & RMSNorm 2", "x = x + Attn(x) | Pre-MLP Normalization", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_arrow(210, 470, 210, 492, stroke="#2b8a3e")

    d.add_box(60, 492, 300, 56, "SwiGLU Feed-Forward (MLP)", "Gate * W1(x) * Swish(W2(x)) * W3(x)\nExpands hidden dimension to 8/3 d_model", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_arrow(210, 548, 210, 570, stroke="#2b8a3e")

    d.add_box(60, 570, 300, 46, "Residual Add 2 -> Unembed Logits", "x = x + MLP(x) -> Output Linear -> Softmax", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # Column 2 (Right Inside Decoder Container): Math & Acceleration Cards (x=370..710, w=340)
    d.add_box(370, 150, 340, 115, "KV Cache (Decoding Acceleration)", [
        "• Prefill: Computes K & V for all prompt tokens in parallel.",
        "• Decode: Appends new token's K, V; avoids O(N²).",
        "• VRAM: 2 * 2 * layers * heads * dim * seq_len.",
        "• GQA shares K, V heads across multiple Q heads."
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(370, 280, 340, 120, "Attention Math & Causal Masking", [
        "• Formula: Softmax((Q K^T / √d_k) + M) * V",
        "• Causal Mask M: Upper-triangular elements set to -∞.",
        "• Tokens attend strictly to previous positions.",
        "• RoPE: Relative distance encoded via complex angle."
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_box(370, 415, 340, 115, "FlashAttention-2 Kernel Tiling", [
        "• SRAM Tiling: Splits Q, K, V into fast on-chip blocks.",
        "• Online Softmax: Eliminates N x N memory writes to HBM.",
        "• Wall-Clock Speedup: 2-4x faster than standard PyTorch.",
        "• Linear Memory: O(N) complexity in seq length."
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(370, 545, 340, 95, "Sampling & Next-Token Generation", [
        "• Temperature: Sharpness (T < 1 greedy, T > 1 diverse).",
        "• Top-p (Nucleus): Dynamic probability cutoff.",
        "• Top-k: Restricts candidate pool to top k logits."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Right Master Container: Distributed Training & Quantization (x=760..1240, w=480, h=605)
    d.add_container(760, 105, 480, 605, label="Distributed Training & Quantization Topologies", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_w=390, badge_align="right")

    d.add_box(780, 150, 440, 85, "1. Tensor Parallelism (TP: Intra-Node NVLink)", [
        "• Splits weight matrices (QKV, MLP) across GPUs on same host.",
        "• Column-parallel -> Row-parallel with All-Reduce communication.",
        "• Requires high-bandwidth (> 900 GB/s NVLink); latency sensitive."
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(780, 250, 440, 85, "2. Pipeline Parallelism (PP: Inter-Node)", [
        "• Partitions 32+ transformer layers across consecutive servers.",
        "• 1F1B schedule interleaves forward/backward passes to cut bubbles.",
        "• Transmits only hidden activations across InfiniBand network."
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(780, 350, 440, 100, "3. Fully Sharded Data Parallel (FSDP / ZeRO-3)", [
        "• ZeRO-1: Shards AdamW optimizer states (8 bytes / parameter).",
        "• ZeRO-2: Shards gradients (2 bytes / parameter in FP16/BF16).",
        "• ZeRO-3: Shards model weights; gathered on-demand via All-Gather.",
        "• Enables training 70B+ parameter models on commodity clusters."
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    d.add_box(780, 465, 440, 105, "4. Quantization & Speculative Decoding", [
        "• Weight Quant (AWQ / GPTQ INT4): Shrinks 70B from 140GB to 35GB.",
        "• FP8 Execution: Uses Native FP8 tensor cores on Hopper GPUs.",
        "• Speculative Decoding: Draft model proposes k tokens;",
        "  Target LLM verifies in 1 forward pass (2-3x speedup)."
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_box(770, 585, 450, 85, "LLM Hardware Scaling Invariant", [
        "• Training is Compute-Bound by matrix multiplies (FLOPs).",
        "• Decoding is Memory-Bandwidth-Bound by weight streaming from HBM."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Master Bottom Banner
    d.add_box(40, 725, 1200, 45, "Architecture Invariant: Pre-RMSNorm + RoPE + GQA + SwiGLU form the core foundation of modern frontier autoregressive LLMs.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("genai-transformer-architecture.png")

def generate_rag():
    d = DiagramBuilder()
    d.add_header(
        "Enterprise Retrieval-Augmented Generation (Advanced RAG) Pipeline",
        "Offline Ingestion, Hybrid Dense + Sparse Search, Reciprocal Rank Fusion, Cross-Encoder Reranker, and Grounded Generation",
        x=40, y=20, w=1220, h=65
    )

    # 1. Left Container: Offline Ingestion (x=40..580, w=540, h=605)
    d.add_container(40, 105, 540, 605, label="1. Offline Knowledge Ingestion & Indexing Pipeline", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_w=400)

    # Row 1: Raw Docs
    d.add_box(60, 150, 500, 50, "Raw Enterprise Knowledge Base", "PDF manuals, Markdown docs, Confluence wikis, SQL records", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=11)
    d.add_arrow(310, 200, 310, 235, label="Document Parsers & Cleaners", stroke="#495057", label_offset_y=-14, label_bg="#ffffff", font_size=11)

    # Row 2: Semantic Chunking
    d.add_box(60, 235, 500, 55, "Semantic & Recursive Chunking", "512-token chunks with 10-20% overlap | Preserves section headings & tags", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_arrow(310, 290, 310, 325, label="Compute Embeddings & Term Frequencies", stroke="#2b8a3e", label_offset_y=-14, label_bg="#ffffff", font_size=11)

    # Row 3: Vector DB & Full-Text Store (Shared Bridge at Row 3!)
    d.add_box(60, 325, 500, 75, "Vector DB & Full-Text Store (Qdrant / PGVector)", [
        "• Dense HNSW Index: 1536/3072-dim embeddings for semantic similarity",
        "• Sparse BM25 Index: Inverted keyword index with exact term frequencies",
        "• Metadata Filter Store: tenant_id, document_id, timestamp, chunk_hash"
    ], bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Row 4: Ingestion Invariants
    d.add_box(60, 435, 500, 140, "Ingestion Architecture Invariants", [
        "• Optimal Chunk Sizing: 256-512 tokens balance semantic density with specificity.",
        "• Metadata Injection: Always embed parent doc title & breadcrumb into each chunk.",
        "• Incremental Updates: CDC pipeline re-chunks and re-indexes modified documents only.",
        "• Embedding Consistency: Query and documents MUST use the exact same embedding model.",
        "• Index Partitioning: Tenant-isolated collection partitions protect multi-tenant security."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # 2. Right Container: Online Query & Generation (x=680..1240, w=560, h=605)
    # Gap between Left and Right = 100px (580 to 680)
    d.add_container(680, 105, 560, 605, label="2. Online Query Processing, Hybrid Retrieval & Synthesis", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_w=430, badge_align="right")

    # Row 1: User Query
    d.add_box(700, 150, 520, 55, "User Query & Transformation (HyDE / Multi-Query)", "Receives user question; decomposes into sub-queries or generates hypothetical answer", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(960, 205, 960, 235, label="Parallel Hybrid Search Query", stroke="#1971c2", label_offset_y=-14, label_bg="#ffffff", font_size=11)

    # Row 2: Query Embedding & Pre-Retrieval
    d.add_box(700, 235, 520, 55, "Query Embedder & Sparse Tokenizer", "Converts query into dense 1536-dim vector + BM25 search terms", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_arrow(960, 290, 960, 325, label="Query Vector DB", stroke="#2b8a3e", label_offset_y=-14, label_bg="#ffffff", font_size=11)

    # Row 3: Hybrid Retrieval & RRF Fusion (Horizontal alignment with Vector DB!)
    d.add_box(700, 325, 520, 75, "Hybrid Retrieval: Dense Vector + Sparse BM25", [
        "• Reciprocal Rank Fusion (RRF: score = sum(1 / (60 + rank))) merges top 50 chunks",
        "• Combines deep semantic understanding (Vector) with exact keyword recall (BM25)",
        "• Pre-filtering: Applies hard metadata filters (e.g. tenant_id == 'corp_a')"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # Connecting Arrow between Vector DB (Row 3 Left) and Hybrid Retrieval (Row 3 Right):
    # Pure horizontal arrow across the 140px gap!
    d.add_arrow(560, 362, 700, 362, label="Top 50 Chunks", stroke="#1971c2", label_offset_y=-16, label_bg="#ffffff", font_size=11)

    # Arrow from Row 3 to Row 4 (Reranker)
    d.add_arrow(960, 400, 960, 435, label="Candidate Chunks", stroke="#2b8a3e", label_offset_y=-14, label_bg="#ffffff", font_size=11)

    # Row 4: Cross-Encoder Reranker
    d.add_box(700, 435, 520, 60, "Cross-Encoder Reranker (Cohere / BGE-Reranker-Large)", "Full cross-attention jointly scores (Query, Chunk); reranks down to top 5 chunks;\nEliminates semantic false positives and boosts retrieval precision by 20-30%", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)
    d.add_arrow(960, 495, 960, 525, label="Top 5 Grounding Chunks", stroke="#f59f00", label_offset_y=-14, label_bg="#ffffff", font_size=11)

    # Row 5: Grounded LLM Generation
    d.add_box(700, 525, 520, 60, "Prompt Augmentation & Grounded LLM Generation", "Synthesizes answer conditioned strictly on retrieved context;\nAttaches citation markers [Source 1] and applies hallucination verification guardrails", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    # Master Invariant Banner
    d.add_box(40, 725, 1200, 45, "Core RAG Invariant: Hybrid Search (Vector + BM25) + Cross-Encoder Reranking reduces hallucinations by over 80% compared to raw vector search.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("genai-rag-pipeline-architecture.png")

if __name__ == "__main__":
    generate_transformer()
    generate_rag()
