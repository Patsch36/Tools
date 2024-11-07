# Contributing to Tools Repository

Thank you for your interest in contributing to the Tools Repository! We appreciate your help in making this project even better.

## How to Contribute

1. **Fork the Repository**  
   Click the "Fork" button in the top right corner of the repository to create a copy of the repository under your GitHub account.

2. **Clone Your Fork**  
   Once you've forked the repository, clone it to your local machine:
   ```bash
   git clone https://github.com/your-username/tools.git
   ```

3. **Create a Branch**  
   Create a new branch to work on your changes:
   ```bash
   git checkout -b feature-name
   ```

4. **Make Changes**  
   Work on your changes locally. Make sure to write clear commit messages explaining the changes you've made.

5. **Commit Your Changes**  
   Once your changes are ready, commit them to your branch:
   ```bash
   git add .
   git commit -m "Added feature-name"
   ```

6. **Push Your Changes**  
   Push your changes to your forked repository:
   ```bash
   git push origin feature-name
   ```

7. **Create a Pull Request (PR)**  
   Go to your forked repository on GitHub and click the "New Pull Request" button. Provide a description of the changes you made and submit the pull request.

## Example Pull Request

#### Title: **Fix: Handle Images Larger Than 10MB in `imgresize.py`**

#### Description:
This PR fixes the issue with resizing images larger than 10MB in the `imgresize.py` script by implementing a check for file size before processing.

**Changes Made:**
1. Added a file size check at the beginning of the script.
2. If the image file size exceeds 10MB, a warning is printed, and the script does not attempt to resize the image.
3. Improved error handling to manage unexpected file types or corrupt images.

**Steps to Verify:**
1. Clone the repository and checkout this branch.
2. Run the script with an image larger than 10MB:
   ```bash
   python imgresize.py --input path/to/large_image.jpg --output path/to/resized_image.jpg --factor 0.5
   ```
3. The script should now output a warning for large images instead of crashing.

**Testing:**
- I tested the fix with multiple images ranging from 5MB to 20MB.
- The script correctly warns the user for images over 10MB and successfully resizes smaller images.

**Related Issue:**
Fixes #12 (Issue: Script `imgresize.py` Fails to Resize Images Larger Than 10MB)

**Checklist:**
- [x] Code follows the PEP 8 style guide
- [x] Tests have been added to verify the fix
- [x] Documentation has been updated (if necessary)
- [ ] I have added an entry to the changelog (if required)

**Screenshots:**
*No screenshots are necessary for this change.*

## Code Style Guidelines

- Please follow the PEP 8 coding style for Python code.
- Write descriptive commit messages that explain why the changes are being made.
- Ensure your code is well-commented and easy to understand.
- If your changes include new features or bug fixes, please add appropriate tests to ensure their correctness.

## Reporting Bugs and Requesting Features

If you find a bug or want to request a new feature, please open an issue on the [Issues page](https://github.com/patsch36/tools/issues).

### Example Issue

#### Title: **Bug: Script `imgresize.py` Fails to Resize Images Larger Than 10MB**

#### Description:
**Environment:**
- OS: Windows 10
- Python version: 3.8
- Repository version: v1.2.0

**Steps to Reproduce:**
1. Run the `imgresize.py` script using the following command:
   ```bash
   python imgresize.py --input path/to/image.jpg --output path/to/resized_image.jpg --factor 0.5
   ```
2. Use an image larger than 10MB.

**Expected Behavior:**
The image should resize and save correctly.

**Actual Behavior:**
The script fails with the following error message:
```
Error: Image file too large, cannot process
```

**Additional Information:**
I have tested the script with smaller images (less than 10MB) and the resizing works fine. This issue seems to be occurring only with images larger than 10MB.

**Suggested Solution:**
The script could use a try-except block to handle large images, or a size check to warn the user that images over 10MB may not work properly.

**Priority:** Medium




