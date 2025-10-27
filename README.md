Problem statement:

School emails are full of information — from the tiny details in the email itself to a dozen attachments. Most of it might not even matter to a parent, depending on the child’s year group or activities.

So the question is: can an agent go through the email and attachments and pull out only the relevant information and send it as a message via telegram?

How we tried to solve it:

We gave n8n a go since it’s popular for building workflows. One reason for using it was that it connects to Gmail using the built-in nodes, and getting authentication set up was fairly simple. But after that, it wasn’t just a case of adding more nodes — some parts needed manual coding, which felt a bit like going around in circles.

The main problem:

Emails often have attachments. n8n has a node to download attachments, but since they come as objects, extracting text from them wasn’t easy. There are some online guides and YouTube videos with possible solutions, but nothing fully automatic.

Going Python:

We decided to try extracting the text with Python. That’s when the real problem hit: data quality. Many attachments were corrupted or compressed, and no Python library could automatically extract the text reliably. We’re still working on fully automating it.

For now, the temporary solution is to manually export the PDF as an image in Preview, then use OCR to read the text and summarise it. Not perfect, but it works.... 

Next steps:

Gmail trigger --> via python app?
Automate pdf -> text 
Refine prompt
send output to telegram

Revist n8n and integrate?
