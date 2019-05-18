# Global-Personal-Financial-Management
Tools to manage your personal finances from any institution, globally

## Specific issues to solve
- Clean and convert raw .csv downloads from financial institution websites
- Standardize transactions to single format
- Create dashboards / reporting

# Thoughts on Personal Financial Management tools
One pain point that I continuously come back to over the years is that in managing my finances. Personal Financial Management (PFM) is something that I've always found fun to do.

## My pain points in PFM
- My entire working career has been outside of the United States. So most of my finances are managed in the local country that I’m working in (China and Singapore).
- There are no aggregator companies that can combine your bank accounts in these local countries so you get an overall picture of how much money you have.
- With accounts in multiple geographies, I often have to mentally compute my net worth with fluctuating exchange rates and multiple accounts across multiple countries
- For existing aggregator accounts in the US, they usually have limited functionality for me to add my foreign bank accounts. Certainly none of them automatically pull my banking transaction history. But many also don’t add the option to manually add my foreign currencies. None of them help me track my foreign currencies converted to US dollar value in real-time FX rates.

I'll try to start solving these problems one by one here.

## Issues that other people face
Even if a bank had an API to check balances and transactions, many of my non-American friends are still not comfortable giving their banking details to a 3rd party to check their bank accounts.

In talking to a few people - mostly friends, a mix of guys and girls, I hear some similarities in pain points as well as a few fresh ones that I’ve never considered.

Though this space is overdone, and there are a lot of players, I think there are still a lot of pain points that none of these solutions fully solve.

There are still tons of people out there that download their statements from their banks and manually manage their expenses on their own spreadsheets.

What makes this problem hard is there are so many different requirements from different people.
- Some people need features that support family finance planning
- Some people want a personal 3-statement format (income statement, balance sheet, cash flow)
- Some people need something to include their crypto currency investments.
- Others have one small feature that’s missing that ends up feeling like a dealbreaker, like missing integration with a certain brokerage.
- Many just hate looking at their finances, scared to see what their spending habits look like and that they might have to course-correct

## My proposal
Create a library of converters that will clean your CSV downloads from your bank accounts, so that you can build your own model from those clean sheets.
Eventually, I’d like to build vertically - providing additional tools to make building your personal financial management models easier.

But I fear taking away the “scratchboard” capabilities of Excel that most people are used to and that they crave.

Every bank account downloads their transactions in a different format.

## Competitor analysis - The good and the bad
The current big players do many good things, but their development has fallen behind.
Mint.com hasn’t been updated in a long time, and is just inundated with ads. You don’t immediately see what you’re looking for on the front page, and it requires a couple of clicks to get to the interesting stuff.

Personalcapital.com also does a pretty good job. Will have to research more of their pain points.

A single recent tweet thread showcased the pain that so many people still face with their PFM and current existing tools.
 
![](F6579E79-FA24-4225-917E-779754343F05.JPG)![](IMG_0242.png)![](IMG_0243.png)![](IMG_0244.png)![](IMG_0245.png)![](IMG_0246.png)![](IMG_0247.jpeg)![](IMG_0248.png)![](IMG_0249.png)
Trying out pocket smith for now. It is mostly premium features. But their tag line and concept is mostly what I’m looking for. They have cash flow forecasts and actually quite a few cool features!
Seeing your cash flows in a calendar format
Seeing your income and expenses across months in a statement format.

Again, biggest issue for them is also a limited free plan. They do have a free plan. But it does not include automatic bank uploads. Which is a game changer, given that Mint and others do it for free.

I am wondering - can I build this and beat them at their own game?
This needs to be geared towards people who don’t care about their finances. People who hate managing their finances - I want to make this more fun for them. I want to get nearly everyone in love with their finances, not just cater to those who are already building their own models in their excel sheets. But I also want to include them.

So one improvement Pocketsmith could do is reduce the pain in the free onboarding session.

There’s so much work that’s required to categorize all of my transactions.
I had to go to Mint.com and download all of my previous transactions.
And my future transactions won’t be included either.

I wonder if I could bring a focus to ~design~ to finance that would bring the larger masses involved. Much like Apple did to technologies that changed the demographics of the technology scene. When iPods and iPhones came out, the demographics skewed more neutrally to include more women than the other competitors did.

Can I make finance more fun, sexy? Can tracking your finances ~give~ something to users that sparks joy?

Some ideas I would like ot try out that I haven’t seen before:
- Let the user decide which premium features they would like to use - for free! But they are only allowed to choose a limited number of them (say 3). This hopefully encourages stickiness. Also hopefully it gives the user the feeling of being gifted with something - a pleasant surprise? If the user wants more than 3, they can subscribe to premium service.
- A voting board (for premium users only) to upvote the feature they want most next. Since PFM there are so many different features required. This will 1) encourage users to contribute by signing up for premium so they can vote, and 2) allow us to surface which feature people are looking for, and are basically deal breakers.
- A chat service that will allow the user to use more natural language to express what they want to do. I would focus live chat bots first with real humans so we can start to really explore what people want. Then start building automated responses for the most common / easy tasks. Ie “how much spent on coffee last month etc.”


Basically, even though Pocketsmith is great, there’s still a big gap and pain point. Whether it’s a marketing issue for them, or that they don’t have a free plan that’s good enough, I think there’s still some room to compete and have winner take all.

Perhaps I can just focus on building something for myself first, and let it slowly grow from there. This would be a good exercise in building a web app - JavaScript / Python back end. Some key features that I’ll need to learn
- Database
- User authentication
- UI / UX

A couple of different problem statements:
1. Lots of people who actively manage their finance, but still use free-form tools (excel) to build their own models and track their finances. This is especially the case outside of the US
2. Lots of people who generally are comfortable with their average rate of income and expenses, and have no desire to track their money.
3. People who really need to manage their money better (living pay check to pay check), but don’t
4. People who don’t invest their savings

But enough with the research. I’ve spent a lot of time deliberating what I want to go into next for this month, and we’re already past halfway through this month with nothing to show for.

It’s time to just code and launch…something!