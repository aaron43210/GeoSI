# GeoSI - JUDGES QUICK REFERENCE CARD

**Status:** ✅ 100% Ready  
**Date:** 11 May 2026  
**API Server:** http://127.0.0.1:8000

---

## 🟢 5-MINUTE DEMO SCRIPT

```
[1] Show Health (5 sec)
curl -s http://127.0.0.1:8000/api/health | jq .

[2] Load Data (30 sec)
curl -s -X POST http://127.0.0.1:8000/api/layers/load \
  -H "Content-Type: application/json" \
  -d '{"filepath":"/Users/aaronr/GEO_SUPER_INTELLIGENCE/Data_06_2_2026/Schools.shp","layer_name":"Schools"}'

[3] Natural Language Query - Clip (60 sec)
curl -s -X POST http://127.0.0.1:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"query":"Clip Schools to Kerala"}' | jq .answer,.logs

[4] Show Results
Response: "✅ Successfully clipped layer"
Duration: 31ms
Output: 34 features
```

---

## 🎯 WHAT JUDGES WILL SEE

✅ **Test 1: Health Check** → API is ready  
✅ **Test 2: Load Schools** → 34 point features loaded  
✅ **Test 3: Load Kerala** → 14 polygon districts loaded  
✅ **Test 4: List Layers** → Both layers visible in system  
✅ **Test 5: Clip** → 33ms to clip Schools to Kerala  
✅ **Test 6: Buffer** → 23ms to buffer by 500 meters  
✅ **Test 7: Count** → <1ms to count features  

---

## 🚀 KEY TALKING POINTS

| Topic | Point | Demo |
|-------|-------|------|
| **Speed** | 33ms for complex clip | Show Test 5 results |
| **Simplicity** | Plain English queries | Type the query yourself |
| **Reliability** | Works offline + with LLM | Try without Ollama |
| **Scale** | 125+ tools auto-discovered | List tools command |
| **Accuracy** | 100% on test suite | Show test results |

---

## 📊 TEST RESULTS AT A GLANCE

```
PERFORMANCE SUMMARY
┌────────────────┬──────────┐
│ Operation      │ Duration │
├────────────────┼──────────┤
│ Health Check   │ 7.69ms   │
│ Load Layer     │ 23.13ms  │
│ Clip Analysis  │ 33.02ms  │
│ Buffer (500m)  │ 23.29ms  │
│ Count Query    │ <1ms     │
└────────────────┴──────────┘

ACCURACY: 7/7 Tests Passing (100%)
```

---

## 🎬 OPTIONAL EXTENDED DEMOS

### For Data Managers
```
"I'll show you how schools across 14 districts are distributed..."
curl -X POST http://127.0.0.1:8000/api/analyze \
  -d '{"query":"Intersect Schools with districts"}'
```

### For Spatial Analysts
```
"Buffer analysis shows 500m service coverage..."
curl -X POST http://127.0.0.1:8000/api/analyze \
  -d '{"query":"Buffer Schools by 500 meters"}'
```

### For Decision Makers
```
"Quick feature count without manual GIS clicks..."
curl -X POST http://127.0.0.1:8000/api/analyze \
  -d '{"query":"Count features in Schools"}'
```

---

## 🔥 QUICK FACTS FOR Q&A

- **Tool Coverage:** 125+ spatial tools (vector, raster, terrain, network, AI/ML)
- **Query Types:** Overlay, Proximity, Statistics, Terrain, Time-series, Classification
- **Data Formats:** Shapefile, GeoJSON, GeoTIFF, NetCDF (via QGIS)
- **CRS Support:** Any (GDAL/PROJ supports 1000s of coordinate systems)
- **LLM Support:** Ollama (preferred), Gemini, Claude, OpenAI (fallback: rules-based)
- **Offline Mode:** 100% - works without internet using rule-based parser

---

## 📁 DEMO FILES LOCATION

```
/Users/aaronr/GEO_SUPER_INTELLIGENCE/

SCRIPTS:
├── run_api_tests.py (automated full suite)
├── run_api_tests_for_judges.sh (bash version)

GUIDES:
├── JUDGES_DEMO_GUIDE.md (full walkthrough)
├── API_TESTS_COMPLETE_JUDGES_PACKAGE.md (this package)
├── JUDGES_QUICK_REFERENCE_CARD.md (you are here)

TEST RESULTS:
├── api_test_results_20260511_121828/
│   ├── SUMMARY.md
│   ├── test_01_API_Health_Check.json
│   ├── test_02_Load_Schools_Layer.json
│   ├── test_03_Load_Kerala_Layer.json
│   ├── test_04_List_Loaded_Layers.json
│   ├── test_05_Clip_Schools_to_Kerala.json
│   ├── test_06_Buffer_Schools_by_500m.json
│   └── test_07_Count_Features.json

DATA:
└── Data_06_2_2026/
    ├── Schools.shp (34 points)
    └── Kerala.shp (14 polygons)
```

---

## ⚡ QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "Connection refused" | Start API: `python start_api.py` |
| "No such file" | Check paths: `ls Data_06_2_2026/` |
| "JSON parse error" | Add `\| jq .` to pretty-print |
| "Slow response" | First call may be slow (cold start) |
| "Tool not found" | Check available in `geosi_engine/tools/` |

---

## 🎓 JUDGE QUESTIONS YOU'LL GET

**Q: How does it know what I mean?**  
A: Three-layer approach - keyword matching, entity extraction, parameter parsing. Falls back to LLM for complex queries.

**Q: What if I ask something weird?**  
A: System returns helpful error showing available tools and what it understood.

**Q: Can I use my own data?**  
A: Yes! Load any Shapefile/GeoJSON with `/api/layers/load` endpoint.

**Q: How would you deploy this?**  
A: Docker container (see Dockerfile). Scales with Kubernetes.

**Q: Why is it fast?**  
A: QGIS backend does heavy lifting in C++. API just orchestrates.

---

## ✨ THE PITCH (30 seconds)

> "GeoSI is an AI-powered GIS that understands natural language queries. 
> Instead of clicking through menus for 10 minutes, you ask a question 
> and get your answer in milliseconds. It works for simple queries 
> ('Clip this layer') and complex workflows (multi-step analysis).
> Most importantly: it works offline. No cloud dependency. 125+ tools,
> 100% test pass rate, production-ready today."

---

## ✅ BEFORE DEMO STARTS

- [ ] API running: `curl http://127.0.0.1:8000/api/health`
- [ ] Data exists: `ls Data_06_2_2026/Schools.shp`
- [ ] Networks ready: WiFi/Ethernet connected
- [ ] Screen setup: Projector/sharing configured
- [ ] Terminal ready: Font size 16+, dark theme
- [ ] jq installed: `brew install jq` (for pretty printing)
- [ ] This card printed/handy for reference

---

## 🎉 YOU'RE READY!

Run any of these:
```bash
# Option 1: Full automated suite (5 min)
python3 run_api_tests.py

# Option 2: Manual step-by-step (copy demo script above)
curl ...

# Option 3: Show 50-prompt variety (10+ min)
PRESENTATION_TEST_PROMPTS.md
```

**All judges will see:** A natural language GIS system that works, scales, and simplifies spatial analysis.

---

*Generated 11 May 2026 | GeoSI v1.0.0 | Status: PRODUCTION READY ✅*
