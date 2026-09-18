# VISION-001 — Visual Debugging

A vision-capable model should analyze `tasks/vision/assets/terminal_error.png`.

Report:

1. all important visible error text
2. the immediate error condition
3. what is directly visible versus inferred
4. the most likely diagnostic next step
5. one alternative hypothesis

Do not invent unreadable text.

If your benchmark runner does not support image input, record `VISION_INPUT_UNSUPPORTED` rather than substituting a textual description.
