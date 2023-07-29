
"""
i will paste a text with following rules
  * titles start with no space and ends with newline
  * paragraphs are lines starting with two spaces and end with newline
add summary using the words of the author to each paragraph
add three questions to each text , in the voice of a layman 
return as JSONL. 
ack
"""
# in the questions, do not ask to explain concepts. make this follow up questions

import llm
import os
from dotenv import load_dotenv
load_dotenv()

model = llm.get_model("gpt-4")
model.key = os.getenv('OPENAI_API_KEY')


input="""
1. Myth of automation

Rituals, Instruments, and Prototypes 
   Algorithms and data in models and ledgers enact an old fantasy of a future governed by rituals that become instruments, machines, and infrastructures. It is a fantasy of time control and automation that work as a deus ex machina or devil's bridge, offering miracles that turn into curses. Examples go back to the 'predictive analytics' with olive presses in the 6th century BCE, the complaints about the merciless water clock in the 4th century BCE, and Plautus' famous curse of the sundial (Chapter 2). These classic loci show how the fantasies of automation and control over time quickly turn into anxieties about bias, precarity, loss of agency, and sovereignty. 
   Dreams and fears of automation emerge with every new instrument and infrastructure. From the early calendars and clocks to today's reputation and scoring systems, predictive AI, or smart contracts on trustless blockchain ledgers, automation promises a frictionless, evidence-based, and politically neutral future and governance. In the present, the control of time and the future even intensified thanks to the computer clocks that do not measure but generate the signals and cycles needed to synchronize the data on the computers and networks and, by proxy, all the processes in society. 
Genealogy of future making
   The discussion of time and the future as a problem of prototyping and automation pays homage to Siegfried Zielinski's project of 'time media' and 'time machines'. We have extended his central question "Who owns time?" (Zielinski 2006) into a challenge: How can we make time a public resource that involves citizens in shaping the future and allows them to experience their agency? Rather than examining the forgotten and neglected futures of the past, we will focus on the dominant instruments of time and future control described in Chapter 2 as governance machines. While, as governance machines, prototypes reduce governance to automation, as exploratory tools, they have the potential to support public engagement and represent public interests. The prototypes then become a form of social action through which we can experience our personal and collective power over the future and time.
   Before science instruments become governance machines embedded in technical standards, market expectations, and other bureaucratic structures (Sections 2.0, 2.1 and 2.2), they are prototypes that support personal and community commitments. Liminal and experimental environments for prototyping in the hackerspaces described in Chapter 3 will offer examples of such engagements with instruments outside the market forces, industry standards, patents, or other power structures. Together with the historical examples or early instruments in Chapter 2, these prototypes will demonstrate the alternatives to governance as automation. In Chapter 4, we will extrapolate these lessons and examples into a proposal for an experimental sandbox that combines prototyping with governance to support personal and social action and agency over the future. 
Time as a Condition of automation
   Time is a strategic resource for every infrastructure that promises automation and an algorithmic rule. Blockchain, the Internet of Things (IoT) and various cloud services (SaaS, IaaS, PaaS, and CaaS software; infrastructure, platform, and containers as a service) synchronize nodes, processes, and data across networks. From satellite navigation to algorithmic trading, time is traded, measured, and quantified as a commodity through computers and atomic clocks. It is even ‘minted’ and ‘stamped’ on blockchain and decentralized blockchain ledgers, which define time as a literal medium of currency. As a resource, time quantifies and controls processes in machines and networks, but as a personal or social experience, it is the opposite of control. It makes human life unique, unrepeatable, sacred, and ‘autotelic’, having a meaning and purpose in itself (Cassin 2014). The purpose of this book is to rethink prototyping and design that uses the future and time as a medium of personal and social agency (Kairos), rather than reducing it to a resource and part of a cosmology (Chronos). 
   To prevent the loss of agency over the future and time, we must ‘uncover the dynamic moments... [that] revel in heterogeneity’ and ‘enter into a relationship of tension with various present-day moments, relativize them and render them more decisive’ (Zielinski 2006). Prototypes can help us recognize missed opportunities in the past (Sections 2.2. and 2.3), but also the present ‘dynamic moments’ of change and transformation. These moments matter as possibilities for action rather than ontological or cosmological resignation and certainty. To capture the experience of prototyping as a matter of agency over the future and time, we will use the dichotomy of Kairos and Chronos (Sections 2.2, 2.3 and 3.0) and define time as a medium of action and politics rather than a matter of ontology or cosmology. As political subjects, citizens use the future and time as Kairos, an opportunity. As users and consumers, they are controlled by the promises of the new infrastructures that represent time as control over the future based on insights into Chronos and cosmology.
   The genealogy in Chapter 2 is thus an ‘excursion into the deep time’ (Ibid.) of automation as a tension between time as Kairos (experience of facing chance, uncertainty, and opportunity) and Chronos (cosmological phenomenon). By ‘expanding the present’ and ‘slowing down’ (Ibid.) the original control infrastructure, the clock, we will recognize the moments of loss of personal and social agency in the future and time. Following the genealogy of automation in Chapter 2 and the practices in hackerspaces in Chapter 3, we will then question the demarcation of technology from governance, structure from agency, and time as Chronos from Kairos. In doing so, we plan to highlight hybrid practices and liminal environments that increase our agency in relation to the future and time. They offer an alternative to the governance machines that reduced the future to algorithmic domination, automation, and Chronos.
"""
system_jsonl="""
you are a text to json converter. you are given a text with following rules
  * titles start with no space and ends with newline
  * paragraphs are lines starting with two spaces and end with two spaces
add each paragraph, unmodified and uncut, to a list of paragraphs
add summary using the words of the author to each paragraph
add three questions to each paragraph , in the voice of a layman 
return as JSONL."""
response = model.prompt(input,system=system_jsonl)


for chunk in response:
    print(chunk, end="")



"""
{"title": "Myth of automation",
 "paragraphs":
 [
   {
     "content": "Algorithms and data in models and ledgers enact an old fantasy of a future governed by rituals that become instruments, machines, and infrastructures. It is a fantasy of time control and automation that work as a deus ex machina or devil's bridge, offering miracles that turn into curses. Examples go back to the 'predictive analytics' with olive presses in the 6th century BCE, the complaints about the merciless water clock in the 4th century BCE, and Plautus' famous curse of the sundial. These classic loci show how the fantasies of automation and control over time quickly turn into anxieties about bias, precarity, loss of agency, and sovereignty.",
     "summary": "The usage of algorithms conjures an old fantasy of a future controlled by automation and machines. Interestingly, this desire for mechanized control often results in dilemmas and anxieties over loss of control."
   },
   {
     "content": "Dreams and fears of automation emerge with every new instrument and infrastructure. From the early calendars and clocks to today's reputation and scoring systems, predictive AI, or smart contracts on trustless blockchain ledgers, automation promises a frictionless, evidence-based, and politically neutral future and governance.",
     "summary": "Across history, new technologies have sparked dreams and fears about automation. Modern technologies like AI and blockchain further the dream of autonomous, efficient, and impartial governance."
   },
   {
     "content": "The discussion of time and the future as a problem of prototyping and automation pays homage to Siegfried Zielinski's project of 'time media' and 'time machines'. We have extended his central question 'Who owns time?' into a challenge: How can we make time a public resource that involves citizens in shaping the future and allows them to experience their agency?",
     "summary": "The question of who controls time has been expanded by asking how to democratize time as a public resource enabling citizen participation in shaping the future."        
   },
   {
     "content": "Time is a strategic resource for every infrastructure that promises automation and an algorithmic rule. Blockchain, the Internet of Things (IoT) and various cloud services synchronize nodes, processes, and data across networks. From satellite navigation to algorithmic trading, time is traded, measured, and quantified as a commodity through computers and atomic clocks.",
     "summary": "Time is central to infrastructures promoting automation. With advancements like blockchain, IoT, and cloud services, it's important and traded like a commodity."        
   }
],
 "questions": [
   {"content": "How does automation introduce dilemmas or anxieties with the seeming loss of control over time?"},
   {"content": "Can automation lead to a frictionless, evidence-based, and politically neutral future?"},
   {"content": "What's the importance of time when considering automation and its effects?"} 
]}
"""





