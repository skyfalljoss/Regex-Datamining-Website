# Regex Data Mining of Websites - Project Documentation

**Team Members:** David Brodosi, Phong Nguyen, Sean Wisk, Trang Dieu Thuy Phan  
**Course:** Automata Theory/Formal Languages (COT4210)
**Date:** November 15, 2025

## 📋 Project Overview

This project demonstrates the practical application of regular expressions and automata theory to extract and categorize URLs from HTML files. The program uses Python and regex patterns to identify different types of links (images, videos, documents, etc.) and exports the results to CSV and Excel formats.

## 📁 Project Files

### Core Program Files
- **`url_extractor_program.py`** - Main executable program (327 lines)

### Test Files
- **`html/test_sample_website.html`** - Sample general website for testing
- **`html/test_ecommerce.html`** - E-commerce page example
- **`html/test_blog.html`** - Blog/article page example

### Documentation
- **`README.md`** - This file (setup and usage instructions)

### Output Examples
- Generated files will include timestamp: `url_extraction_results_YYYYMMDD_HHMMSS.xlsx`

## 🚀 Setup Instructions

### Prerequisites

1. **Python 3.7+** installed on your system
   - Check version: `python --version` or `python3 --version`

2. **Required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

### Installation

1. Download all project files to a directory:
   ```
      project-folder/
      ├── html/
      │   ├── test_blog.html
      │   ├── test_ecommerce.html
      │   └── test_sample_website.html
      ├── results/
      │   ├── url_extraction_results_20251114_235000.txt
      │   └── url_extraction_results_20251114_235000.json
      ├── final-report.md
      ├── presentation-slides.md
      ├── README.md
      ├── requirements.txt
      ├── sources.txt
      └── url_extractor_program.py
   ```

2. Navigate to the project directory:
   ```bash
   cd project-folder
   ```

3. Verify installation:
   ```bash
   python url_extractor_program.py --help
   ```

## 💻 Usage

### Basic Usage

```bash
python url_extractor_program.py *.html
```

### Expected Output

The program will:
1. **Print to console:**
   ```
   Processing: https://www.usf.edu
   Processing: html/test_blog.html
   Processing: html/test_ecommerce.html
   Processing: html/test_sample_website.html

   ======================================================================
   EXTRACTION SUMMARY
   ======================================================================

   Total Sources Processed (URLs/files): 4
   Total URLs Found: 171

   Per-Source Breakdown:
   ----------------------------------------------------------------------

   https://www.usf.edu: 130 URLs
   - Anchor Link: 1
   - Image: 12
   - Script/Style: 9
   - Webpage: 108

   html/test_blog.html: 13 URLs
   - Archive: 1
   - Document: 3
   - Image: 1
   - Script/Style: 3
   - Webpage: 5

   html/test_ecommerce.html: 12 URLs
   - Document: 2
   - Script/Style: 1
   - Video: 2
   - Webpage: 7

   html/test_sample_website.html: 16 URLs
   - Archive: 2
   - Audio: 1
   - Document: 2
   - Image: 2
   - Script/Style: 5
   - Video: 1
   - Webpage: 3

   Results exported to: ./results/url_extraction_results_20251114_235000.xlsx

   Results exported to: ./results/url_extraction_results_20251114_235000.csv
   ```

2. **Generate Excel file:**
   - Filename: `results/url_extraction_results_20251120_184530.xlsx`
   - Sheet 1: "All URLs" - Complete list with columns: Source File, URL, URL Type, Category
   - Sheet 2: "Summary" - Per-file statistics with category counts

3. **Generate CSV file:**
   - Filename: `results/url_extraction_results_20251120_184530.csv`
   - Same data as Excel for compatibility

## 📊 Understanding the Output

### URL Types

The program identifies three types of URL structures:

1. **Complete URL** - Full URL with protocol
   - Example: `https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=400&fit=crop`
   
2. **Protocol-Relative** - Inherits protocol from parent page
   - Example: `//cdn.example.com/script.js`
   
3. **Absolute Path** - Path from domain root
   - Example: `/images/logo.png`

### Categories

URLs are automatically categorized into 7 types:

| Category | Extensions | Examples |
|----------|------------|----------|
| **Image** | jpg, jpeg, png, gif, bmp, svg, webp, ico | `photo.jpg`, `logo.png` |
| **Video** | mp4, avi, mov, wmv, flv, webm, mkv | `demo.mp4`, `tutorial.avi` |
| **Audio** | mp3, wav, ogg, flac, aac, m4a | `podcast.mp3`, `music.wav` |
| **Document** | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, csv | `manual.pdf`, `report.xlsx` |
| **Script/Style** | js, css | `main.js`, `style.css` |
| **Archive** | zip, rar, tar, gz, 7z | `files.zip`, `backup.tar.gz` |
| **Webpage** | All others or no extension | `https://example.com/about` |

### Special Link Types

The program also detects:
- **Anchor Links** - `#section` (jumps within page)
- **Email Links** - `mailto:info@example.com`
- **Phone Links** - `tel:+1234567890`

## 🧪 Testing the Program

### Using Provided Test Files

Test with the included HTML files:
```bash
python url_extractor_program.py 
```

**Expected Results:**
- test_sample_website.html: 16 URLs
- test_ecommerce.html: 12 URLs
- test_blog.html: 13 URLs
- https://www.usf.edu: 130
- **Total: 171 URLs across 7 categories**

### Creating Your Own Test Files

1. Create an HTML file with various link types:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <link rel="stylesheet" href="/style.css">
   </head>
   <body>
       <a href="https://example.com">Link</a>
       <img src="/images/photo.jpg">
       <script src="https://cdn.example.com/script.js"></script>
   </body>
   </html>
   ```

2. Save as `my_test.html`

3. Add `my_test.html` to `sources.txt`

4. Run the extractor:
   ```bash
   python url_extractor_program.py
   ```


## 🔍 Troubleshooting

### Common Issues

**Issue 1: "Module not found" error**
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution:**
```bash
pip install pandas openpyxl  requests et-xmlfile
```
or
```bash
pip install -r requirements.txt

```


**Issue 2: Excel export fails**
```
Error exporting to Excel
Falling back to CSV export...
```
**Solution:** This is normal if `openpyxl` is not installed. CSV output is generated automatically as backup.


## 🧠 Key Concepts Demonstrated

This project showcases understanding of:

### Automata Theory
- **Finite Automata (DFA/NFA)** - Each regex pattern represents a state machine
- **Regular Languages** - URLs follow regular patterns recognizable by finite automata
- **Pattern Matching** - Using regex for string recognition
- **Kleene Operations** - Star (`*`), plus (`+`), and alternation (`|`)

### Software Engineering
- **Object-Oriented Programming** - URLExtractor class design
- **File I/O** - Reading HTML, writing CSV/Excel
- **Data Processing** - Extraction, categorization, deduplication
- **Error Handling** - Graceful failure and fallback mechanisms
- **Testing** - Comprehensive test files and validation

### Practical Applications
- **Web Scraping** - Extracting data from HTML
- **Data Analysis** - Categorizing and summarizing URLs
- **Export Workflows** - CSV and Excel output for further analysis

## 📈 Performance Characteristics

- **Time Complexity:** O(n·m) where n = HTML file size, m = number of regex patterns
- **Space Complexity:** O(k) where k = number of unique URLs found
- **Processing Speed:** < 10ms per typical HTML file (< 100KB)
- **Scalability:** Linear scaling with file size and number of files

