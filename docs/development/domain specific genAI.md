# interview with AI expert

After earning his PhD simulating jet engines and leading GE's digital twin revolution, he's helping Articul8 build domain-specific AI solutions for the world's most complex industries, from Wall Street to electrical grids and aerospace design. Arun joins us on today's show to explore the challenges and opportunities of deploying AI in legacy industries like manufacturing, financial services, supply chain and aerospace. Our conversation dives deep to explain why after years of investment, enterprises often struggle to turn data into actionable intelligence and how generative AI is shifting that paradigm.

Arun discusses why general purpose models, no matter how powerful, are insufficient on their own for high-stakes domains and how organizations are increasingly relying on domain-specific models and orchestration frameworks to move beyond table stakes. But first, are you driving AI transformation at your organization? Or maybe you're guiding critical decisions on AI investments, strategy or deployment?

Absolutely. You know, just in light of what we're seeing in very large legacy industries, when it comes to AI adoption, and before we're digging into specific use cases, I think it's helpful to start by exploring some of the foundational challenges for what we're seeing in sectors like manufacturing, supply chain, B2B financial services, and energy, a few others. You know, deploying AI isn't just a matter of plugging into a model and getting answers.

These are industries defined by complex processes, specialized terminology and data that's mostly locked behind secure perimeters. Despite years of investment in data infrastructure too, I think many organizations that we hear from on the program still struggle to turn that data into actionable intelligence, moving from siloed systems to regulatory restraints. But even just from the 10,000 foot level, thinking about where the roadblocks are, where are you seeing the big slowdowns for enterprises that they face when trying to get real business value out of their existing data?

Yeah. So first of all, the context is very relevant, right? So the industry across the board, whether it's financial services, manufacturing, supply chain, aerospace, whatever that might be, the investment in data has been pretty consistent across almost a decade or more.

And that investment was done on the basis of a potential ROI that also has pretty much study after study has shown that we haven't reached there. And the predominant reason for that really is, one is that you still need to put in a significant amount of high quality talent into trying to get the data to be useful first. And after the data gets cleaned in a state that is useful, then you have to go start building applications with it.

It's those two bottlenecks that have been like slowing things down to getting to production, number one. And the second one is, even if you get something to production, to keep it in production, you have to have the same teams working tirelessly to making sure that the data doesn't get corrupted. The data is actually continuing to be at high quality.

Today, the advantage of GenAI really is the ability to shorten that cycle quite a bit and also be able to do that in a way that is consistent and repeatable. And what I mean by that is, instead of thinking about moving all of your data into one place, like say normalizing it, standardizing it and then using it, imagine going from your messy sources of information, which by the way is only going to get even more and even faster and then more messier by the day, into applications as quickly as possible. So as you're processing, the application is also consuming it.

So it's not necessarily a two-step process, it's actually a continuous process. That's really the biggest shift that we are starting to see. And in terms of the investment that have gone in, that's really what is fueling this transformation as well.

But people have to move intentionally towards that. But I can give you some specific examples around how they can go about doing that in different industries as well.

Yeah, let's start there and we'll dive into a little bit more of what we're seeing in terms of the rubber hitting the road between the challenges and the technology.

Take a simple example, right? So take like there's disparate industries, maybe between finance and manufacturing, they're as different an industry as it can get. But from a data perspective and from the perspective of hitting applications, that's something that is a very common problem, which is data comes from different sources.

They may not all be at the same level of quality, and you also do not have the data in exactly the same formats that you want to consume. Take even a simple example, you have a set of PDFs that you have in your enterprise. You have a set of Word documents, you have a set of Excel files, you have a set of PowerPoint documents.

All of them are there. You want to answer a question. And the question might be in the financial services world, you want to say what is the investment risk on a particular company based on their learnings and all of the data that you have locally.

Now you have publicly available information and you have private information that you have from your own research and your own analysis. You have to mix them together and you have to figure out between texts, images, tables, understand all of those things together before you can even present an answer to the user. Now imagine what, say, an internet search would do, a Google search would do.

It's just looking at websites and then getting you back answers here. You have to go analyze something before getting an answer. That analysis part was what was blocking you before.

Now imagine if a set of models are analyzing, before giving you an answer. And that piece, whether you are in financial services or in a manufacturing company or in an aerospace company or in a supply chain company, the base problem of data is more or less the same.

Right, right. And as we often say on the program, so many problems across industries, intellectually, you would never assume have anything in common, look the same from the perspective of data. That being said, you know, aerospace, financial services, supply chain, we see crossover, supply chain involves an element of aerospace.

These are all legacy industries. But even outside of the challenges, how much do these organizations look the same in terms of their mechanics from the lens of data?

That's a very good point. So the organizations look remarkably similar, meaning you have the CIO's office and perhaps the CTO's office, they have their own data management teams, and then they have the application teams, they have to work together. And in a lot of times, it is that level of, say, siloed behavior that gets into a conversation where how do you get to the data that you need to build an application, which to your original question of getting to business value or business outcomes, really is what starts the whole conversation.

Now, imagine if a business owner who wants, who understands the business value, who needs to do, say, for example, an analysis for an investment they're making or they are looking for figuring out what is the next, say, sales channel they can go run or a particular go-to-market exercise they can go execute. They want to know what product has been used by whom, what customer has said what, what they want to know, what is our competitor doing, what features were potentially considered delightful, all of those different pieces of information. They would have to go do their own work in pulling information from different places together.

Now, imagine that an enterprise has all this information within it. It is really the glue that comes together and pulls all of these things together that actually gets you to your outcomes. The machinery behind the scenes that actually runs this to get you to the outcome is remarkably similar.

Absolutely. I think there's been a lot of changing in the language of how we talk about a lot of these models, especially since the explosion of LLMs that we saw not too long ago. I'll dive into the differences between how we used to talk about them then now in a moment.

But there are general purpose AI models. I think we see a lot of these on the market. Very much as we dive into this topic, if you want to explain how general AI models, where they are in the buy versus build conversation, I think is very valuable.

But these general purpose AI models, why aren't they particularly useful for high stakes domains like these spaces, like aerospace, like finance, like supply chain? I think even where we used to talk about them as foundational models, even just a few years ago, the assumption was, oh, you'll have one at the heart of the organization, but then it'll bifurcate out. Of course, the conversation has changed a lot since then.

But it seems as though the tenor is we don't want to even use these general purpose ones, even what we called foundational not too long ago, really at all in these domains. But why is that?

I would say they're really necessary, but not sufficient to get to high-value use cases. The analogy I'll really give you is really the core thesis of why Articul8, the company even exists because we are a domain-specific GEN AI platform, catering to industries that require high degrees of accuracy and high degrees of value. The reason for that is, think of the analogy where the general purpose models, by the way, they've become very useful and for general purpose tasks, they are extremely capable.

That's why I mentioned that they are required, but not necessarily sufficient. Think of them as maybe at the proficiency level of answering questions or interacting with you at a high school level. Because they have learned everything that is there to learn from the general internet, but they don't necessarily know the difference between what is considered high quality and what is considered not so high quality.

That's really where it is. They can understand the language. Now, if you start building domain specific models that understand that particular domain, by what I mean by that is like say a financial services domain specific model understands the nuances of the finance industry.

And it's like talking to a college graduate who understands who has a degree in finance. And that would be a domain specific model. Now, you take that domain specific model and then deploy that into an enterprise and then continue to train that model with the enterprise's own practices and best practices and datasets.

That becomes an advanced user from that particular enterprise itself. It's very similar to hiring somebody from fresh out of college and then them having 20 years of experience in a company. So that's the analogy I'll make.

That becomes an advanced user from that particular enterprise itself. It's very similar to hiring somebody from fresh out of college and then them having 20 years of experience in a company. So that's the analogy I'll make.

But they're all built on top of each other.

And back when these generally would get called foundational models, the idea was you'd have that as something of a mothership, and then all of these ancillary models around it. Is that model, for lack of a better way of putting it, is that system, that framework still relevant?

That's why we call it a model mesh. Think of it as a collection of models working together, very similar to how humans work together as well, where it's not any one expert that you rely on, it's really a team of experts. And it's really the team or the group of models that work together, each one is specialized in one thing.

And you may also have multiple general purpose models that actually are good at certain things versus certain other things. For example, there are some general purpose models that are very good at coding. There are some other models that are very good at translation.

This material may be protected by copyright.
So you may have both of them running. With domain-specific models that understand your particular domain, that work together. Now the trick there is, how do you know which models to call for what?

How do you know how they work together? That's not an easy problem to solve.

Of course. And basically coordinating all of these models and their specific boots on the ground business applications often gets put under this umbrella called orchestration. Very interested if we can give that maybe a harder definition than maybe the folks out there tuning in have heard before.

But wondering what's involved in orchestration between this model mesh framework as you're presenting it and how it helps enterprises leapfrog legacy systems and really wake up that data that's in their tech stack for generative AI.

So I think the reason why we named it Model Mesh is it's really like personifies what it actually does, which is there is no set rules in terms of if this happens, then do that. The reason for that is think about humans. When you are asked a question or when you're presented with a situation, you assess the context of the situation before you answer the question.

For example, if an elementary school student asks you a question and a college graduate asks you the same question, you might answer it very differently because you know the context, you know who's asking it. Whereas if you ask the same question to the same model, more or less, you will get similar answers. It's because it doesn't understand context.

Whereas if you just go with orchestration, which by the way is really defining flows of how all of these different pieces are connected together and they work together. That's what I would call orchestration. What Emerj does is an autonomous orchestration, which means that there are some general guidelines of if you want to answer a question, it goes to a particular way.

But based on the question, based on the context, based on the data you have access to, it decides a few different paths and it might explore all of those paths before getting you to an answer. That's pretty much what happens in our mind, but that's the decision logic that happens behind the scenes when we talk about model mesh. Now, that also has evolved over the last couple of years.

If you heard of models like DeepSeat, that became the rage about six or seven months ago, it's because they showed that an individual model can reason. Meaning when you ask a question, it says, how the user is asking this, let me think about this, and then it actually exposes what seems like a thought process before it gives you an answer. That's called a reasoning model.

Think of the model mesh as a reasoning system. When you ask the question, you say, okay, is this question simple enough for me to answer directly, or should I break it down into four or five questions? Go fetch the answer to each of those questions, and then combine the answer before I gave you an answer.

That's why you need a full-blown reasoning system. And interestingly enough, that's where the industry also is gone, where now you hear the word agents a lot. And agents are models that are combined with tools that can reason.

So you can say, you were asked a question, you say, oh, maybe I need to go do a web search for it. So that's a tool that goes and does a web search, comes back, gets the results back, and then gives you an answer. That's one agent.

Really, to get you to an outcome, model mesh is an agent of agents. It's multiple models working together with multiple tools, doing different things and coming in, presenting an answer to you.

The entire mesh of models is that mothership. The agents are the poops on the ground. Yeah, the individuals.

And they can actually go work together. And the way they work together is also dependent on what you're asking them to do, right? So I'll give you some examples of that as well.

Sorry. What I mean by coordination is, for example, if you ask a question like, hey, what is the investment profile for Tesla? And it gives me an answer by comparing how much Tesla has invested in R&D compared to their revenues and compare that to auto manufacturers in the US and Japan.

Now, I just sent a natural question in a matter of 30 seconds. However, if you break that down, it's four or five or six questions that you need to answer before you get to a final answer to the user. And the answer also doesn't exist anywhere, meaning I can't read a report which has the answer to that exact question.

I need to get multiple pieces of information from different places together to get to a final inferred answer. Now, humans do that today. I go ask Google Search or even say, any of the search tools, I'll get different answers and then merge them together in my head.

Think of the agents of agents doing that for the user almost at the 90 percent or 95th percentile. That's where it's getting to be a lot more useful. Where what used to be super delightful, getting an answer from Google Search used to be super delightful.

They're not necessarily be anymore, unfortunately, because it's just a bunch of links. You need more. That's where it is all being enabled by a lot of these agents and bringing it back to enterprises.

All of this capability exists for the consumer world. For the first time ever, if you notice, the consumer world has access to super advanced technology before enterprises do. It used to be that all this was so expensive that only enterprises had mainframes, only enterprises had these large computing systems, and eventually it will make it to the consumer world.

Here, it's happening in reverse, meaning almost every single business leader I've talked to, every single business I go to across the globe, everybody is using some AI tool in their personal life. Maybe even in their professional life may not necessarily be completely approved, meaning they go ask a question somewhere else and then they copy paste stuff. It may not be completely safe, but they may not put all of their company data there.

But the percentage of business users using AI globally, like whether it's North America, South America, Europe, Asia, that percentage is clearly about the 80-90 percent mark. The question is, if that is the case, first of all, they are doing that to, of course, boost their own productivity, they're getting usefulness, they can get access to it. But if most of those tools don't have access to the internal core data sets, what you would call the crown jewel of data sets.

Now, imagine the value it will unlock. If any user in the company who's authorized to see the data, it's not like you're giving it to everybody in the company. The people who have the authority to see the data and access the data can actually take advantage of the data set.

Now, that gives you a significant advantage compared to all of your competitors. Because there's two other things you mentioned in terms of enterprise challenge. Right now, the challenge is to get things to production.

So, yes, these systems are hard to get to production. There are a lot of decisions to be made. You don't know which models to use.

We don't know which providers to go to. I'll be a bit self-critical here. Just like Articul8, there are 10,000 other companies who are hitting up all of the CIOs saying, hey, my solution is better than somebody else's solution.

How do you even decide whom to use? I would like tell to those leaders the challenge is real, but it almost doesn't matter. The reason I say that is inaction is far worse than action that you need to change a little bit of time.

If you start somewhere and you learn that that tool was not good enough, it's fine. You can change. Not starting will put you behind in ways that are very difficult to get out of.

That's one thing. The second piece is actually a little bit more subtle and also bigger challenge, which is no matter what you do, pretty much all of your competitors are also going to get there eventually because a lot of these technologies are becoming table stakes. And unless you use your own data set, your own processes to get an advantage with these systems, everybody else is going to eventually get to the same level of sophistication as you"

An example I'll give you is say you use GitHub Copilot or you're using say Microsoft Copilots to say edit your PowerPoints, edit your Word documents or whatever it might be. So can all of your competitors. The performance boost that you got, everybody else would get the same performance boost as well.

The difference is your data, the difference is your people, the difference is your outcomes. And if you can bottle that in ways that only you have access to, you'll clearly see a differentiation. And that's what we're seeing repeatedly all over the place where enterprises who have figured out that no matter who we picked, there's always going to be somebody else who does slightly better than that, but doesn't matter.

Actually, Trump's not moving.

Right, right. And at that point, so you come across the decision, we've heard it many times on the show, you got to jump in the pool, try to make it the shallow end, but don't wait to jump in the pool. But at that point, then the next question inevitably becomes ROI.

You've talked a lot about, you do want to measure potentially different partners or any kind of buy situation through this criteria, but don't let that stop you from getting started. Once you've started, how are you thinking about ROI potentially with partners, especially when it comes to generating AI systems and building them into this orchestration format?

Absolutely. In fact, we are very clear about not starting unless a customer already has some means of measuring an outcome. And the reason for that is, if it's just a cool AI project, it's not something that you want to get started because it's a cool AI project that will sit in the shelf.

You really want to have at least some notion of measurement, either from this sense of scale, like so meaning how much data you're processing, from the sense of accuracy, from the sense of speed. Those three things are critical because without those three things, you're not going to get to a production system. You can say, I processed 100 documents into the school report, but it's not repeatable.

That's one. And the second side of the story is, is there somebody in the business who's signing up for, if you do this, there is actually business value. And usually it's not that hard to do because you are already faced with enough number of business challenges that you can't solve.

Pick one that you cannot solve because if you're picking one that's a pure productivity play, that is going to get you to a table stakes conversation very quickly. Versus if you're going and picking one that is hard to do today or close to impossible to do today, the measurement is incontrovertible. There's no subjectivity around the measurement.

And with a lot of these systems, the hype is so much that if you show a 5%, 10% delta, it's not something that is going to show up. Why? Because you're already seeing two times to five times to ten times difference in the consumer applications you're already using.

Many times, for example, internally, we challenge our teams to say, look, we are doing this, but then an external tool is doing this with no effort.

Right.

Right? So we need to be way better than this, not just do the same thing that an external tool would do.

And we see this in LLMs even from an editorial perspective of, great if it didn't take you four hours to write that piece, but is it taking you three and a half hours to adjudicate what the LLM gave you, then are we really saving time? And is the quality there for that extra 30 minutes that you gained? Am I seeing 30 minutes of a better material come out of it?

So it's not even like, time spend necessarily isn't the only metric we're judging that by. And great to hear, especially from so many areas where experts and executives are hearing, go for the low-hanging fruit, go for the low-hanging fruit is not all made equal. More or less what I'm hearing in your answer.

In fact, we are squarely in the domain. Today, I would argue, and people would disagree with me, it's just a personal opinion, is that going for the low-hanging fruit is making sure that you are going after table stakes use cases. And the reason is most of the low-hanging fruit will be taken care by any one of the tools that you already have.

I'll tell you, a simple thing is like a note taker, or any, say, document editing system. Like if you want simple things like that, most of the tools that you use will have that as an option that comes in automatically with no additional cost, versus you having to go do a use case that is considered fundamentally differentiating. That is the opportunity that you have in front of you today.

Like why, which business leader would say they don't want to tackle a use case that's a 10x use case? The difference really is the 10x use cases that were out of reach, that used to be a super stretch goal, is now in reach and doable without actually breaking your budget or making that a heroic effort.

Low-hanging fruit refers to the ease of which deployment, not the size of the deployment, not the stakes of the deployment, which can be quite a misnomer. Really, really important to emphasize. It might seem obvious to a few, but sometimes you got to say the quiet part out loud.

And we really appreciate you coming on the show Arun and doing that for us, especially with the multi, we're up on another hype cycle with agentic AI systems. And especially now that we've had hype cycles so close to each other and we're remembering, oh, do we need this level of skepticism? It's very important to separate, hey, here's what has changed.

And here's what we're starting to see isn't changing much and staying consistent no matter what systems we're using. Arun, thank you so much for being with us this week.

Thank you so much for taking the time.

Wrapping up today's episode, I think we heard a number of takeaways from our conversation with Arun today, but here are four we'd like to summarize for leaders across industries and financial services, aerospace, supply chain, and manufacturing. First, general AI models are necessary but not sufficient. General purpose models are like high school students, capable in broad tasks, but ill-equipped for critical decisions in specialized domains.

Second, combining multiple models and tools dynamically allows enterprises to reason, analyze, and deliver answers that no single model could. Third, low-hanging fruit often leads to undifferentiated capabilities. Leaders should prioritize use cases that are hard to achieve today, but transformational.

And finally, AI projects must tie to measurable outcomes. Scale, accuracy, or speed to avoid becoming shelf-wear and ensure lasting impact. Are you driving AI transformation at your organization, or maybe you're guiding critical decisions on AI investments, strategy, or deployment?