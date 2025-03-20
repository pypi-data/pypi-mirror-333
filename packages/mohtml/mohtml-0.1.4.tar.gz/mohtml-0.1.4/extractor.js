// extractor.js
// A utility to extract code from markdown codeblocks and open it in a new tab as part of a query string

class CodeExtractor {
    constructor(config = {}) {
      // Default configuration
      this.config = {
        // The URL template to open, with {code} being replaced by the extracted code
        urlTemplate: "https://example.com/search?q={code}",
        // Selector for code blocks (default: all <pre><code> elements)
        selector: "pre > code",
        // Whether to encode the code for use in a URL
        encodeForUrl: true,
        // Maximum length of code to include in URL (0 = no limit)
        maxLength: 0,
        // What to do if code exceeds maxLength: 'truncate' or 'error'
        maxLengthBehavior: 'truncate',
        // Whether to show a button next to each code block
        showButtons: true,
        // Custom button text
        buttonText: "Open in new tab",
        // Custom button styles (CSS object)
        buttonStyles: {
          position: 'absolute',
          top: '5px',
          right: '5px',
          padding: '5px 8px',
          backgroundColor: '#4285f4',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '12px'
        },
        ...config
      };
  
      // Initialize if auto-initialize is enabled
      if (this.config.autoInit !== false) {
        this.init();
      }
    }
  
    init() {
      // Process markdown configuration if provided
      this.processMarkdownConfig();
      
      // Initialize buttons if showButtons is enabled
      if (this.config.showButtons) {
        this.addButtonsToCodeBlocks();
      }
  
      // Return this for chaining
      return this;
    }
  
    processMarkdownConfig() {
      // Look for HTML comments with JSON configuration
      const configComments = document.querySelectorAll('*');
      let foundConfig = false;
  
      for (const element of configComments) {
        const commentNodes = Array.from(element.childNodes)
          .filter(node => node.nodeType === Node.COMMENT_NODE);
        
        for (const comment of commentNodes) {
          const text = comment.textContent.trim();
          if (text.startsWith('CodeExtractor:')) {
            try {
              const jsonConfig = text.substring('CodeExtractor:'.length).trim();
              const parsedConfig = JSON.parse(jsonConfig);
              this.config = { ...this.config, ...parsedConfig };
              foundConfig = true;
              console.log('Found and applied CodeExtractor configuration:', parsedConfig);
            } catch (e) {
              console.error('Error parsing CodeExtractor configuration:', e);
            }
          }
        }
  
        if (foundConfig) break;
      }
    }
  
    addButtonsToCodeBlocks() {
      // Find all code blocks matching the selector
      const codeBlocks = document.querySelectorAll(this.config.selector);
      
      codeBlocks.forEach(codeBlock => {
        // Create a wrapper if the code block isn't already in one
        const parent = codeBlock.parentElement;
        if (parent.tagName.toLowerCase() === 'pre') {
          if (getComputedStyle(parent).position === 'static') {
            parent.style.position = 'relative';
          }
          
          // Create button
          const button = document.createElement('button');
          button.textContent = this.config.buttonText;
          
          // Apply styles
          Object.entries(this.config.buttonStyles).forEach(([property, value]) => {
            button.style[property] = value;
          });
          
          // Add click event
          button.addEventListener('click', (e) => {
            e.preventDefault();
            this.extractAndOpenCode(codeBlock);
          });
          
          // Add button to parent
          parent.appendChild(button);
        }
      });
    }
  
    extractAndOpenCode(codeBlock) {
      // Extract code from the code block
      let code = codeBlock.textContent;
      
      // Check if we need to limit the length
      if (this.config.maxLength > 0 && code.length > this.config.maxLength) {
        if (this.config.maxLengthBehavior === 'truncate') {
          code = code.substring(0, this.config.maxLength);
        } else if (this.config.maxLengthBehavior === 'error') {
          alert(`Code exceeds maximum length of ${this.config.maxLength} characters.`);
          return;
        }
      }
      
      // Encode for URL if needed
      if (this.config.encodeForUrl) {
        code = encodeURIComponent(code);
      }
      
      // Replace the {code} placeholder in the URL template
      const url = this.config.urlTemplate.replace('{code}', code);
      
      // Open the URL in a new tab
      window.open(url, '_blank');
    }
  
    // Public API to manually extract and open code
    extractFromElement(selector) {
      const element = document.querySelector(selector);
      if (element) {
        this.extractAndOpenCode(element);
      } else {
        console.error(`Element not found: ${selector}`);
      }
    }
  }
  
  // Example usage:
  // 1. Basic initialization with default settings
  // const extractor = new CodeExtractor();
  
  // 2. Custom configuration
  // const extractor = new CodeExtractor({
  //   urlTemplate: "https://jsfiddle.net/api/post/library/pure/?code={code}",
  //   buttonText: "Open in JSFiddle"
  // });
  
  // 3. Manual extraction
  // document.querySelector('#extractButton').addEventListener('click', () => {
  //   extractor.extractFromElement('#myCode');
  // });
  
  // Export for use as a module
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = CodeExtractor;
  } else {
    // Make available globally
    window.CodeExtractor = CodeExtractor;
  }