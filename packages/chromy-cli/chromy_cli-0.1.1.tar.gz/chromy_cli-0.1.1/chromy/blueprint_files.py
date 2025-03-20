POPUP_HTML = \
"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{}</title>
    <link rel="stylesheet" href="popup.css">
</head>
<body>
    <h1>{}</h1>
    <p>{}</p>
</body>
</html>
"""

POPUP_CSS = \
"""* {
    margin: 0;
    padding: 0;
}
"""

POPUP_JS = ""


OPTIONS_HTML = \
"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{} Settings</title>
    <link rel="stylesheet" href="options.css">
</head>
<body>
    <h1>{} Configuration</h1>
    <!-- Add options page here -->
</body>
</html>
"""

OPTIONS_CSS = \
"""* {
    margin: 0;
    padding: 0;
}
"""

OPTIONS_JS = ""


BACKGROUND_JS = \
"""\
chrome.runtime.onInstalled.addListener(function (details) {
  if (details.previousVersion) {
    return;
  } else {
    // Run code here after first installation
  }
});
"""


CONTENT_JS = \
"""

"""