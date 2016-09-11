We have a real world demo of Waiter at https://youtu.be/62WCHLGV5eU!

This project is covered by Techcrunch!

https://techcrunch.com/2016/09/11/waiter-will-wait-on-hold-for-you-and-call-you-back-when-a-representative-answers/

## Inspiration

We have all suffered from long phone waits. Banks, mobile phone companies, government agencies, hospitals.. you name it. When you are put on-hold, there is nothing you can do except for being extremely patient and trying not to lose the connection or you will have to start all over again.

## What it does

With Waiter, you don't have to wait any more! When you are put on-hold, you can simply hang up, and our smart voice-based bot will automatically take your position in the waiting, until it detects some real person picks up the phone, in which case it will give you a callback.

Waiter does not require any signup or installation. It doesn't even require a smart phone! The only communication between you and waiter is through the phone itself. You simply dial Waiter's number, tells it which phone number you wanna reach, and hangs up when you are put on-hold.

## How we built it

In a nutshell, we first use Twilio and Google Speech recognition API to implement a simple Turing test bot to detect whether a human agent is online or not.

We then use Twilio's conference call APIs to implement the main user flow. The main reason for using the conference call is that we need to connect three parties together: the user, the callee, and the bot.

## Challenges we ran into

- The accuracy of Twilio's own transcription engine is not very good. We have to switch to Google Speech API, which is much better.
- Speech recognition is slow for all the services we tried, and that incurs significant delay in our Turing test, and hurts user experience.
- Initially we tried to simply detect human speaking in the incoming phone audio, but that didn't work out very well, as many helpdesks included advertisements in their recorded holding audio. We then changed to a challenge-response-based Turing test, which worked much better.

## Accomplishments that we're proud of

- Twilio + Google Speech API bot. It does recognize words pretty well :)
- Figured out a user flow that requires nothing other than a phone, and does everything with Twilio's APIs.

## What we learned

- It is certainly possible to build smart voice-based bot to interact with human or other automated voice systems.
- Personal bots can be very useful in helping with many daily mundane tasks.
- The accuracy of speech recognition is pretty satisfactory in our testing, but the speed of speech recognition might still be a bottleneck in realizing a good user experience when communicating with bots.

## What's next for Waiter

- Keep on improving the user experience by reducing delays.
- Extending Waiter to other voice-based tasks.


