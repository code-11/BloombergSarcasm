from textblob import TextBlob
from itertools import imap

from samr.data import Datapoint
from samr.predictor import PhraseSentimentPredictor

from sklearn.cross_validation import KFold

import httplib
import json
import urllib
import os
import glob


#Forgive us for putting the data in-line. These two lists were collected by hand from itunes.
sarcastic_text=["Wow, another free update!!!?! I don't feel right downloading an update for this app, for free, after it has given my family so much. I sent a check to Samsung for all this app has done but they refused to cash it. I'm left with only one option, to pledge my first born son's life to them.",
"The mysterious ways of push My grades were suffering. I had a bad job, very few friends, and I was partially deaf. Then this app came into my life, and all of a sudden life took a 180. I became valedictorian of my class, got a huge raise, and I hear clear as the sunny skies. God bless Samsung push service, and America.",
"The push i need I dont know what this app really do, but I come here whenever I'm in the toilet doing the second stuff and need some extra force push. Thanks everyone, thanks Samsung, thanks Push Service.",
"Awesome! Outstanding! 5* Before I start this review I would just like to tell you a few things about myself I was an alcoholic a drug user I snorted anything I can get my hands on cough syrup air fresheners you name it, but thanks to Sumsong's Push Service app my life could not get any better I immediately went to counceling to help my drug addiction and have been sober for 10 years now also I have written 10 novels and became the very first person to win over 20 pulitzer prizes. Thank you sumdong you just saved my life.",
"All I can say is wow. I was in a dead end job, and didn't think things could ever get worse. Then I downloaded this app. Since installing this on my phone I got $100/hr raise and got a new girlfriend, and my other girlfriend and wife don't mind at all. I also developed x-ray vision and can fly. Well I can't consider it flying yet, it's more like hovering but still way better than having to stand up. Thanks Samsung.",
"Laid and sex This app will get you laid. ... install it and guys and girls will want you in their bed. Not Gay? Don't worry. They'll rape you. Cut you up in pieces and put you in a river. This app has magical Powers too. It will take your money and deposit it in my account.",
"Most useless app in the history of mankind Going by the reviews....which are comical as they come....state that this app nevertheless is absolutely 100% useless....and for samsung to come with an update for it...is sheer stupidity....now...lemme update it so that I can push my spaceshuttle out of the mud.....ALL ABOARRD!!",
"great thanks sams for the push i was low in life, my gf left me, my grades went down, my salary was too low... then miracle happened.. i got push... now i can fly like supe with my underwear in!! got a job , hot gal friend and sexy spouse... I have a Lamborghini of gold n diamond... have a resort in Nanda parvet.. Batman pays daily visit... thanks sams fr ur push....",
"Push Services Are Alright I Suppose I have IBS with constipation, but this app does just what it was intended to do (by reading my biorhythms it notifies me of when i can push for maximum effect) and lessens the amount of time spent on the toilet, which is really great; it's time better spent with my children that would normally be bothering me from the opposite side of the door. Now all I have to worry about are these hemorrhoids. Thanks Samsung!",
"Push me ill Push u back Thanx 4 the Push Samsung if it wasnt 4 u id still b homeless and eating out of garage cans now im a top excutitive in a 500 company I have tons of friends and lots of moola. If and when I need another Push ill let u know.",
"Beyond reality. Since the recent update, I have joined the cast of Sliders which has allowed me to travel amongst different dimensions and worlds. Don't know what I would have done without you Samsung. I'd still be stuck on planet Desta3. Since being pushed to new world's I have spawned my ability to comment as other users, thus allowing me to share everything about all my other lives!",
"Unable to tell. But seriously if you are going to slam Samsung please don't give the app 3, 4, or 5 stars. I'm new to the Android world , this is my 1st Android ) and frankly I liked my Windows phone much better.",
"When push turned to shove Everything was great with Samsung Push Service, when ever I was feeling down, I got the push to get back up. But it wasn't long until Samsung got too pushy, I didn't feel safe when I had my phone on me, it vibrated if I didn't pay enough attention to it. I tried pulling the battery, but it only got angrier, I would trip because some strange force pushed me to the ground. I'm writing this on a laptop, if your reading this, its too late, delete this app beforeyvguvgyyvgvgyivvvvvvvvvvvvvvvvvvvvvv",
"The push that saved my life!! So me and my best friend was hiking on a cliff then suddenly I slipped and fell down but luckily I got a grab on a small rock I extended my hand to my friend for help but he couldn't get to me..just a few inches gap.I was loosing the grip and I prayed to the god then suddenly I felt my phone vibrating in my pocket and it was the Push service..It gave me a hard push and I was able to get my friend's hand.Thanks Samsung I owe my life to this app!!",
"OMG!! i was stuck inside a toilet bow and i need someone to push me out!but there is nobody nearby me that can push me out,luckily,my phone's notification tab blinking and it push me out!thank you very much!",
"always pushin' that's what sammy is alll about, pushing people. like why dude, why?! I'm so outraged. every time I turn around, sammy pushin meh. don't you understand, sammy, that none of us care about you pushin. go push a log out instead!",
"Just when i had lost all hope..... I had been wandering the seedy back alleys of town for hours, looking for my a reason to go on, looking for a real 'fix'. After being accosted by the low life scumbags who reside in this suburban ghetto for what seemed to be the hundredth time, i was ready to give up on it all. Then BAM, samsung became my savior, my guardian angel. It emerged from the shadows and offered me a free fix, saying 'Hey kid, you wanna fly? The first trip is on me, just remember where you got your ticket'. Now i have samsung on my speed dial, to summarize; samsung is the best pusher, ever.",
"Astounding Initially I refused to update this app that seemed pointless. . Today it updated itself. 5mins later Kim Stamp, Raquel Reign, Catya Washington, Shenecka Adams and Khrysti Hill(all women with ASSets) all show up on my doorstep in Nigeria begging me to date them.. 2 mins later the banks gave me unlimited access to their funds. Hawai here i come. THANK YOU SAMSUNG !!!",
"Push pushed me to Push, naturally. The other day I was at a genuine low, eating tuna out of the can and talking to all my cats and my plant about the last romantic comedy we cried over on the sofa in my bathrobe and glasses. Then, overnight, my new push came. I awoke with gorgeous flowy red hair and a new life outlook. I opened my closet to find a pair of Loubotons and push-up bras aside a new silky bathrobe. The new young mailman came to the door...it's like everything I need just falls into my lap. Thanks, push!",
"Samsung push service pushed me to take a different phone brand. Never again will I purchase samsung ever again.",
"Amazing and inspirational Thanks for this Push Service, Samsung. You have truly out done yourself. Ever since I had installed this app, I had noticed a rather obvious change in my life... a source of courage... you could even say something along the lines of an extra push. I had four starving orphans show up at my house, begging for food and shelter. All I needed was a push to close the door, and Samsung provided me with that. This is the best app on the market, any good Christian can't be caught without it. 1 download = 1 prayer",
"The best part of waking up I've had a secret crush on the neighbor girl for years, but never had the confidence to do anything about it since I was pantsed in front of her by Butch Farland. She's got a huge following on social media and posts countless photos of celebrities and herself on boats, planes, at parties,etc. After a particularly juicy photo with her and Ryan Gosling showed up on my FB wall I had all but given up until Push updated. I walked right up and kissed her on the mouth and learned she'd loved me the whole time.",
"I figured rate 5stars so I'm not going to be hacked or put on a samsung terrorist Watch List?",
"Before I installed this app, I was a mediocre apprentice who couldn't master the most basic force powers. After installing this app, my life changed dramatically as I mastered my first Force Push. The other force powers came to me like they were native. The other apprentices are now simply jealous of me. Thank you Samsung!",
"Thank god for Samsung push. If it wasn't for this regular reminder to read these reviews, my life would be a total Mess. Thanks to all you really funny who give me something to laugh at each update. You guys and girls rock.",
"That vital power to push!! I was stuck, the walls were closing in. inch by inch they were closing the gap between each other and I was stuck! At this point it was an inevitable death for me, I wondered how I'll look, maybe like a red gooey slush of crushed flesh with bone fragments like nuts on a sundae. Then it happened, I suddenly realised my Samsung push service, and after activating it, it was like I hand this new energy inside me. And boy did I push.. I pushed and pushed and pushed with all my strength till finally......",
"This completes my soul Atop Mt. Everest I roared a mighty roar as the Martians cast the remains of the donkey-hugging ISIS members into the incinerator. 'Samsung Push Service Ackbar!!!'",
"Gave me that push I needed I was lost in life. Popping pills starving myself . Crying for nothing. Then 1 day my friend told me how this app changed her life. I installed it & next day I was cured from it all!! I work 12 hr shifts and own a home & 2 cars now! This app gave me that push I was searching for & needed!!",
"Went to jail cause of this app Me and my girlfriend went hiking the day i was gonna propose, we reached the top and i was about to take the ring out, but something happened. She received an update from google and jumped down. It was Samsung. I swear i didnt do it. Samsung pushed her.",
"Life changing I was standing on a mountain valley, having a constant thought of climbing that beautiful large mountain, but my physique didn't allow me to climb it. I gave up. But then, almighty Samsung gave me that extra push to get to the top. ....And now..... I'm on the top. Thank you Samsung, thank you",
"Saved me from certain death So I was on my rollerblades going down the ramp to jump the 20 shark infested falming school busses as i do on the daily, and something went wrong with my launch. I was going too slow and was about to face a flame filled shark mauling educational death when all of a sudden I got a push from samsung push service and it gave me the extra speed I needed to make the jump, I know it was prbably a one off chance, but whenever I jump now I still keep my trusty S5 and SIII in my pocket. Thanks Samsung",
"Wow, where do I start? One drunken night I found myself in a bad part of town and unable to find my way out. I walked street to street long for a familiar landmark to no avail. Well, my wandering must have drawn the ire of some local street toughs, because faster than you can say 'shallow grave' I found myself surrounded. Just when I thought it would be my end, out of nowhere a hooded savior beat my assaulters to a pulp. As they left they said Samsung Push in the Play Store! Rate it 3 stars at least! And here I am.",
"I just love the other reviews Whenever I feel bored and amazon reviews don't satisfy me anymore, i come to google play to have a good read.",
"Freedom Just because of this app people in Albania will be able to gain their freedom from the dictatorship. They will finally be free. God bless this app. God bless Samsung",
"Greatest app EVER! I have been in 5 rehabs, 2 psych wards, 3 jails, and countless hospitals and detox clinics... And nothing has had so profound an impact on my life as Samsung push service app. Updating this app resulted in an indescribable spiritual experience. The very moment I pushed 'update', the clouds parted, harps played, & a ray of sunlight shined on my face. I really can't explain it, but the obsession to drink and do drugs has inexplicably vanished. The 12 steps have nothing on Samsung push service!",
"Push service clears me up Its great. I spend almost no time taking a crap anymore. Samsung's push service has my bowels cleared in no time",
"Just when i had lost all hope..... I had been wandering the seedy back alleys of town for hours, looking for my a reason to go on, looking for a real 'fix'. After being accosted by the low life scumbags who reside in this suburban ghetto for what seemed to be the hundredth time, i was ready to give up on it all. Then BAM, samsung became my savior, my guardian angel. It emerged from the shadows and offered me a free fix, saying 'Hey kid, you wanna fly? The first trip is on me, just remember where you got your ticket'. Now i have samsung on my speed dial, to summarize; samsung is the best pusher, ever.",
"Samsung helped me. There I was, on top of Mount Doom about to throw the ring into the fire when something pushed me to keep the ring for myself and pawn it for millions of dollars. Because of you Samsung I am now the richest hobbit in all of middle earth. I married Liv Tyler and have a great view in my condo in Naples.",
"Pushed me down a cliff When I was feeling helpless, I updated this app and I instantly felt like my life was fullfilled. Since the I never looked back and now I am aiming at becoming the president of the United States",
"Altered my state of conciousness Samsung push service offered enlightenment after a life long journey one night. I found satory and became one with the universe.",
"Great for pregnant women. Works especially well in the ninth month. If you're hoping for twins, run it twice. Should have 6 stars!",
"Omg My name is barry allen.and im the fastest man alive.when i was a child i saw my mother get killed by the impossible.today I AM the impossible. Because i installed the app i am now superfast and i can travel at the speed of light. I am the FLASH",
"I am so ripped I started P90X3 and boy is it tough! I was trying to do those plyometric push ups and I hit the wall (the floor, actually). With my last ounce of strength I reached out for my phone and activated the Samsung Push Service. Suddenly I felt a push that lifted me up off the floor and filled me with strength and determination. Now I can do military push ups, wide push ups, staggered push ups, even the push ups where you clap your hands in the middle, all in sets of 50. Thank you Samsung Push Service!",
"Pusherman My drug sales slowed down but since getting this update awww Mann I'm looking to retire early and bang hot chicks till I'm 90. I love u samsung",
"You don't always need a push! Last week I took my family to visit the Grand Canyon, I've never had to ask Samsung for a push before so I've never used it but after the update Samsung took it upon itself to give me my first push and it caused me to fall down the canyon... I ended up breaking both of my legs and three ribs, thanks a lot Samsung.",
"I love this app it does everything i expected it to do! Wait what does this app do? I think it makes my dinner but dont know how to do that",
"KABOOM POW I don't even have a Samsung and this app works great. I am no longer blind, can speak 38 languages, run a 5k marathon in 1.7 miles, and created a new chat service called wrekt.me",
"Wow I won the lottery I just hit the update button and a million dollar ticket fell out my phone thank you Samsung!",
"Push me harder After updating this app, I felt complete..happy.. It's everything I could ask for. Yesterday and the days before that I was feeling down, depress, suicidal but since I update my Push Services, oh boy! Oh boy! After feeling that very hard, good push, that I've been missing all my life, I just wanna do it all the time.",
"A good push helps when you have eaten too much cheese. Thanks Samsung! Now I can fit into my mankini again!",
"A Miracle This app gave birth so my wife was saved the pain and she had even more time for this app which pushed the baby out with pure ease fanatic Samsung Thanks soooo much!!!",
"Great in top stores Pushes the trolley for me in Fortnums so my butler can have a rest",
"ONE PUSH! Before getting this app, it took me about 2 hours just to use the bathroom. Now it only takes just ONE push and I'm done! Thank You Samsung!",
"Saved my baby I was in the middle of labour and my babies head got stuck for around 5 hours but then my phone vibrated and this app gave her the push she needed! Thanks Samsung",
"LMAO These reviews are so frigging funny. Laughing so hard my bellybutton pushed out:)",
"Saved me from the YMCA This app is a life saver! I used to have to dance for all the men and boys at the YMCA for my Push Services addiction. Then Samsung came along and gave out free updates. Thankyou Samsung you have given this dancer a new look on life!",
"The Push I Needed I was desperate. Alone. I was severely overweight and lost all hope in life. And then I got Samsung Push Service. In mere days I was back on track again and my life regained its meaning. All because of that one little Push... God bless Samsung",
"Made life worth living Was feeling low lately but saw this update for Samsung Push and decided to do something with life, I now have a 100k a year job and looking to buy my 3rd private jet. Thanks Push!",
"I so happy. *I can see youve finally updated the description* Couldn't be happier that I installed the update to be installed if needed update. I didn't update the install. Seriously. Samsung, how about you actually read what your putting out in the public domain. Retarded descriptions are so 2005... Great comments from the rest of you lucky enough to stumble across this little gem.",
"Nice hair This app has changed my life it has made my hair start to grow again after years of being bald and now supermodels are flocking to my door thanks samsung you have turned my life around this app also turned my battered old datsun car in to a brand new jag I now cant wait for the next update as I hope to get a helicopter",
"From South Boston: Im amazed at how much my own life has changed since I bought a Samsung Galaxy and Push has entered my life! I used to be a size 36A bra , not now ...with PUSH i have grown to a 36DD !!! Men cant help but stare and I cant help but let them!!! Thank God for Push ..giving me the extra pushhh I needed to get that Boob Job! Thanks Again for everything !",
"Mr Worn out After I installed this app my boss gave me a $50,000 payrise and advised me I only need to work 2 days a week instead of 5 and my big fella grew another 4 inches and Swedish blonde twins knocked on my front asking for a 3some. App is just amazing how I lived without it is beyond me and I won lotto that very weekend. Samsung push app is life changing. Samsung need one for the iPhone",
"I was so greatful When Samsung could push me anywhere I wanted to go, in demand for free!",
"Like WoW. World of Warcraft. That is how wow this is. I cant explain it. Its just... like wow. No words. Just like having your face smashed against a wall or something. FAB",
"Zesty Thanks to the Samsung Push Service my hair is always shiney and flake free. My clothes have less static cling and the accompanying sounds of mating deer it emits are a delight.",
"Thanks you! Just went back in time and I met my ancestors. Thanks push thing.",
"From january 1st Samsung Push Service Will be used aroung the world in child birth complications so those women who can't push, now can get a push from Samsung. Thank u samsung for saving millions of lives in advance...",
"The best After installing it, i stared at a brick wall and absorbed some sort of a power into my chest. Now i can FUS-RO-DAH all day. Thank you Samsung for making me Dragonborn.",
"Why so serious? I used to be too serious, never cutting loose, never taking chances. Then I downloaded the push service... its pushed me to be a better man, to lighten up, and to take risks. Where would I be without you push service? WHERE?",
"The most important update It was a dark and stormy night. The rain was beating down and I was traversing through the narrow roads of the mountain. My bicycle's chain broke and I was forced to push the bike up. If it weren't for this app's push, I wouldn't have been able to make it to the top. Thanks Samsung!",
"Its happy feeling for my jonny Push....push & push and bang it hard 10 times a day ..complete satisfaction for hotties....hot ladies. ..try me and get full satisfaction. I have Samsung push service on my jonny",
"The Samsung Cure For the longest time I could not figure out how to push buttons. So, I went to the local hospital to figure out my condition. The doctors diagnosed me with a rare disease called Pushidous. He explained to me that there is no cure for this disease unless I go buy a Samsung phone and download Samsung Push Service. I then proceeded to fill the doctors tasks. After my purchase, I could push any button that crosses my path! There is no button that can withstand my button pushing force. Thanks Samsung and doctor!",
"THIS APP SAVED MY LIFE AGAIN I was drunk as f*ck again. Then suddenly i ran out of beer. Good god this app pushed me a beer right over from the counter. Id give 5 stars if it was vodka...thanks again samsung !",
"Definitely Pushin me! I have no idea why so many people posted irrelevant comments on this app. This is such a amazing fancy app which definitely push me to switch to iPhone. Thank you SAM-never boring-SUNG",
"Bestest This update made my phone into a more super duper super genius. My truck now puts out 1000hp &1000 torque. My 4 year old scored 3200 on the SAT and I can now spin a basketball on my toes. Awesome update. Keep up the great work!",
"I just won the lottery! I used the stats from the star ratings for Samsung Push to help me choose my lotto numbers and I won 468 million! And straight after I installed the update Rosamund Pike walked into my house and asked me out on a date! Thank you Samsung Push!",
"I love it Thanks to this update pushing out my farts smell like fresh chocolate chip cookies.",
"Life at last! It's was hectic! It had been hours! Still nothing. She had now been in labour for 16 days! Doctors didn't know what to do! Until an alien space ship dropped through the window and brought the Samsung push service hero to us! In 20 seconds flat, she popped out our sons! All 9 of them! That's almost 2 seconds a son! Thank you Samsung push service! All 11 of us! Papa tisa!",
"Was very chilled until.... My finger said, move quick I'm going to burst into flames! Great app if you like scar tissue on finger and buying new phones because flash has melted",
"SEEMS LEGIT. I never knew that my table was so stressed out! THANK YOU SO MUCH for making this app. Now I know that I must take better care of my table. For all you people with stressed tables, I recommend taking it out for a jog once in a while to reduce stress. Also, drinking Chamomile tea is an excellent way as well.",
"Well to first off start this review I would like to explain how I now have split my life time. It is almost like the conventional system of B.C and B.C.E. And yes I am comparing the birth of Christ to the app. So This is how I have split my life B.I.I.D.O.(before is it dark outside) and A.I.I.D.O.(after is it dark outside). Yes it has really changed my life that much. I know my place in this world I am no longer a slave to the old human hassle of being unable to determine if it is dark outside. It has all changed. I can now actually know if it is dark, I can define dark... I am dark, except when it's light. So when the average man asks me if I should download this app, I say a simple 'yes'. As not to confused this person who's mental capacity is being taken up by determining if it is light or dark, I don't wanto to startle them. There mind will be free now because of this app and the true meaning of life can be reached.",
"This app has deeply and truly changed my life. Before I had this app, my life was nothing. I didn't even know if it was light or dark outside. I now not only know if it is light or dark outside, but I now know the true definition of light and dark. This app allows me to be one with the darkness and one with the lightness that is outside. Now I am sure that some of you will read these reviews and decide to never get the app, but I'm telling you GET THE APP. Now, that is all my child, go off and get the app...",
"This revolutionary app allows you to see if it's dark outside- without even getting up!! This app has changed my life. I've been waiting centuries for an app like this to come out. It's especially useful when my vampire friends and I don't know if it's safe to go outside yet. This app is so breathtaking and I recommend you stop whatever you are doing and download this RIGHT NOW!",
"Thanks gmmm and is it dark outside. Myself and my tablet have always felt a sense of loneliness that we could not satisfy until now. This app overwhelmed us with how superb, unbelievable, extraordinary, magnificent, gratifying, unattainable, perfect, joyful, glorious, monumental the content of this app provides. Thank you so very much. I <3 red pandas",
"I love this app and who ever made should get a noble peace prize for making a vampire life saving app! If your in a closet afraid of the sun like Howy from bench warmers then this is just for you! I love it thank you so much you might have saved my life. You should make it 99cents because it would be worth it!",
"Most Luxurious Application- Due to its helpfulness during applicable situations, I believe 'Is it dark outside?' is worthy of more than five stars. This app is helpful in many different situations including but not limited to: Waking up at a random time and not having the capability of going outside. Being to lazy to get up. Not having the curtains open. More! You can almost feel the enthusiasm from myself oozing through your screen! Most of all, this app is completely free, unless you are annoyed by the small amount of ads. So I encourage you all to download this app!",
"This app is so amazing make me want to cry instead of opening a curtain right behind me I can go through 50 steps to see if it is light or dark like all you gamers go out for food when it gets dark cause we be raising to each other! Beautiful app!",
"I was lost in the stormy clouds of my own failure until I found this app. It's complete, mind-melting absolution gave my heart just the strength to love my woman with the strength of seven suns. Than you, THANK YOU is it dark outside app. I can say with certainty that it is NOT dark outside, app. God bless America.",
"I have done some testing. Over the last ten minutes I have had this app, it has been 100% accurate. It totally knows that it is not dark out!! This must be magic!!!",
"I used to live a boring routine life where I have to do everything for myself, with this app I no longer need to trouble myself and I'm waiting on the ( is someone in the bathroom) app... This way my life will be complete..",
"Wow, words can't even begin to describe how much this app has changed me, it has made my life so much easier. This deserves more than 5 stars. I would highly recommend it to prisoners. It works great !",
"This app has changed my life since I got it. Before I got this app I was lost and had to use all my muscles to look outside to see if it was dark, be now I can gain more weight sitting and eating food and eat Twinkies.",
"Bruh this app is everything. I was honestly suicidal because I thought my life had no meaning. Then this app came around and changed EVERYTHING! All the time I saved by not looking outside I accomplished all my dreams.",
"This app is amazing! Just shows how advanced modern technology is! Why is this free????? Make it 2.99!!! Highly recommend this app to my hamster!!!!!!! It's that easy to use!!!!! MAKE A PRO EDITION!!!!!!",
"I cannot describe the wonders this app has worked in my life. It never fails to amaze me with its accuracy. So much easier than getting up and peeking out my window or even looking at the top of my phone screen to see what time it is. Brings me to tears.",
"Being a werewolf like myself is quite hard sometimes living in a cave and all. With this app I now can figure out when to hunt and when to just go have fun with a stick or ball",
"After finding out this had an apple watch feature, i emptied out my entire life savings and bought the 17 thousand dollar apple watch!!! So worth it to have this app on there!",
"I have been given the gift of knowledge. When I saw this app, it was as if God himself had come down and given me the answers to all of my problems. Thank you for this app!",
"This app is the most amazing thing in ever. Instead of looking slight to the left I can go through 30 steps to see if it is dark. Simply amazing"]



non_sarcastic_text=[
"I've never written a review before, but this app is such a hit with my 14 month old granddaughter, I thought I should share that!  She absolutely loves the song and the options of three different styles (western, rock and pop)  All the interactive things to touch also thrill her--the cat under the bed, the dog at the window, bouncing ball, lamp that makes everything go dark and so on.  Be warned, though, everytime she spots my Kindle Fire, she HAS to play the 'Monkey Game.'", #B004A9SDD8
"does not let you sample only for a sec. if you download  it to computer it talk your music you have try to sell it back to too. if you join with a membership and if you don't pay they  sell your music on your computer . how when you combine your to there player . i know cause the did it to me had rhapsody a long time unit  it happen i close the account . don't mine paying. but not for music i have  before that . had the old look . at the time now it worse", #B004AFQAUA
"Ive been purchasing Rhapsody for 4 years now. Its absolutly invaluable!! I love that you can download songs for use out of service. Other than public radio its all I'll listen too!", #B004AFQAUA
"Does not work in B&W;, image comes out in high contrastcolor mode works better, but it does not focus the camera so the document is blurry", #B004AGCR1K
"This is  a great! It pops up and you can devotions from a number  of people! but nothing is better that The scriptures daily!", #B004AHBBPW
"The ad really talks up the 'Free' aspect.  The app is free and calls within the US are free.  Calls outside of the US require setting up an account to purchase minutes.", #B004ALFHV2
"I guess I abuse my Droid X with all of the apps I run and settings I play with. That used to mean a daily pop-out of the battery to get everything running smoothly again. I couldn't believe the claims the Fast Reboot Pro folks made for this app but tried it anyway. Now, I go months without having to reboot the old-fashioned way. It takes about 5 to 10 seconds for Reboot to do its work. Much quicker than powering the phone down and pulling the battery.", #B004ALJIOE
"if u like bloons defense then ur gonna love this. its just like tht. don't listen to other coments its realle fun", #B004ALVL6W
"i love this it helps when my kindle is sluggish or an app wont workits like rebooting without rebooting!!", #B004AMAIZQ
"Endless supply of puzzles, functions great! Lots of options for all levels of skill. I would definitely recommend this, and it is free!", #B004AMDC86
"this game cheats.  don't understand how the game wins when it has one ball left and hits the 8 ball in and wins. imdeleting this game", #B004AMFUYK
"horrible graphics, audio, gameplay and control.  intact,  nothing good to say about it.  even the free one is not worth the space it takes up in memory.", #B004AMLATE
"Finally. After several thousand years of the same dull, out-of-date gragger technology, someone has had enough of the whole boring-gragger megillah! Take your Purim to Esther 2.0-level.Grag in modern style! Get this awesome app!", #B004AMRGLA
"It does what it is suppose to do, and it can come really handful at times.It doesn't really have to be a car, it can be anything else! You're just marking down the location where you are at, if you are ever lost at a place you're unknown to it, this will come in handy.", #B004ANC00Q
"This app provides more info than I imagined and is also customizable to make it convenient and easy to use.", #B004ANMWPY
"We are cutting back on our cable cost--using Amazon Prime, HULU plus, and Netflix for tv/movies, and cutting down to the lowest tier of cable (until we get an antenna installed) and getting Ooma reduces our cable cost by $100 per month.  With the lowest tier of cable--basic reception--you don't get the on-screen tv grid.  This APP is a fine substitute.", #B004ANMWPY
"I'd give it five stars but I'm not clever enough for anything beyond &#34;Moderate&#34;. You lose a star because I can't play half the levels. It ain't fair, I know, but, well... that are life.", #B004AZH4C8
"controls are really bad. seems like no matter how you move the phone it just goes where it wants. gfx are decent. wouldnt recommend payin for it", #B004AZSY4K
"Enjoyable word game but would prefer the capability to move to the SD card.  Hence, my decision to give 4 stars.  It would also be nice to be able to have a high score screen, a la Bejeweled2, rather than just single personal best.", #B004BN3YQE
"It is a fun game to sit and relax with.  I love being able to choose the different categories.  I can avoid the ones I know little about.  Even the ones I am very familiar with give me a nice level of challenge.  I want to see even more categories for me to choose from.", #B004BN3YQE
"keeps your brain working. fun.I like both puzzle &amp; arcade but the puzzle is great for fircrd problem solving. thats great for my kids. helps keep them focused.", #B004C4FL5Y
"I like the fact that you can make your own background and can use the bubble gun; however, my favorite part, and my son's, is that it is ad free! This means that he isn't screaming for me every few minutes because he accidentally hit an ad... If the ads aren't an issue for you stick to the free one.", #B004C4FL9A
"I was looking for a good thesaurus to use in my writings. This hit the mark. Now I know I can count on finding just the right word.", #B004CN7Y4G
"I've tried several call recorders on my motorola citrus and none of them worked at all. This one will crash if you try to play an empty save, but other than that it works perfectly. The volume is good even when not on speaker. Both sides of the conversation are clear as a bell. Awesome app.", #B004DJZBN0
"love the idea but almost impossible for them to have all hh on here. not nearly enough places listed. great if u wanna drive 20 miles at 9 at night for a drink", #B004DK37V2
"Really enjoy this version!! Love that it keeps track of all games played and gives your average! a real keeper", #B004DKSUXC
"This version of spider is a bit easier to win since it gives you options that some others don't. It still takes some skill but it is a cut above some of the others", #B004DKWCAO
"Only two chordshapes are presented .  The A (barre) shape and the &#34;D&#34; shape.  The &#34;G&#34; shape is not included.", #B004DL7DJ8
"This is a very simple app. I don't know when I'll need to use it, but it's nice to have on my Kindle when I do need it.", #B004DLLNFS
"Honestly I have just been using this for a morning and am VERY impressed.  It runs very smooth on my rooted thunderbolt running uber bamf preview3. I cannot understand all the negative reviews.  this app needs some work and is not perfect images are a tiny bit grainy.  Overall worth a download!almost ready for paid app status.", #B004DLNBDA
"Very buggy, laggy, limited customization, bland, extra themes cost money, looks like low resolution on the clock, and overall lame. Good concept but horrible execution. Unless your phone is crap, don't waste your time. Installed it on a HTC Thunderbolt.", #B004DLNBDA
"Pretty bad ass i must say! Love the interface! Works really well surprisingly and flows nicely.  Was just listening where cops were after a motorcyclist on the golden gate bridge.", #B004DLNC4I
"I got this app for my Android phone and my kindle fire. I have definitely enjoyed it on both. No complaints here!", #B004DLNC4I
"Keep abreast of local incidents with this scanner. Easy to use, with a large range and choice of listening preferences.", #B004DLNC4I
"Downloaded with no problem.Most recent 6 books downloaded with it. Could read on tablet no problem. Removed, though, because required too much memory for just 6 books.", #B004DLPXAO
"I have had no problems with kindle.  It seems to be an excellent product for my needs. I would highly recommend it especially for android tablet users.  Works great on mine.", #B004DLPXAO
"Don't know how I ever lived without this !!The only problem that I seem to have is after reading a book is finding it ro do a review. I'm sure its an user error", #B004DLPXAO
"I tried and tried to make it work and only got adds and more adds. Uninstalled it. I want a plain hangman game", #B004JJXVYK
"Doesn't work at allWhy is there a 25 word minimum for opinions? What a waste of time for me typing and for you reading this.", #B004JK07LO
"My 8 year old daughter likes this app and plays on the bus with her buddies going to school.  It helps to increase her vocabulary - hopefully, good words depending on who she sits with on the bus.", #B004JK2CCG
"Still keeps telling me to download and upgrade.  Categories are boring.  No easy, medium, hard or expert settings which would be nice..", #B004JK34GO
"It looks really bad, like the kind of graphics that are typical of a free app. Unfortunately, I've seen betterand this game is usually $2. If it was more fun, it might be worth it, but this was just too boring.", #B004JK5X9A
"I use K-9 Mail on a daily basis, and it's a great email program.  Had no problems connecting to imap or pop3 accounts, has lots of configuration options (really like that I can set a 'quiet time' for notifications), and does everything I need it to.", #B004JK61K0
"I've been using PhoneWeaver since it first was developed for Windows Mobile a few years ago.The Android version is even better!  Very stable and reliable on my EVO 4G.Developer continues to add new features and make sure it works well on various devices.", #B004JK681W
"Full disclosure: I've become pretty jaded (pun intended) by 'gem games'.  I mean, how many different ways can you 'swap 2 to match 3'?  Gem Spinner puts a different twist on it, as you don't just 'swap two' gems -- you 'spin' a group of them.  So from that standpoint, this game does put a new 'spin' (yeah, pun intended again) on an old game.  But what I found is that it is very difficult to determine exactly which gems are going to 'spin', and where they will land up.  So trying to create any kind of strategy becomes extremely difficult.  I suppose that if I spent hours and hours on it, it'd begin to get a bit more predictable.  I just got frustrated before that time came.", #B004JK7CBM
"I rarely use this. It is cumbersome.  I have the app on another device and it works much better.  Not something I would recommend.", #B004JK9EYA
"I love this app because of the cool things u can do the price is right for this app and the first time I played with it it was hard to understand but if you know art like me you get it! So so so cool you have to get it!!", #B004JK9Y36
"To address issues noted in other reviews: when you open it, you will see that Galaxy Tab is not yet supported. As I don't have a Galaxy Tab, I didn't check to see if it claims to support it. Buying extras: yep, if you need more cheats or helps to finish levels, you will have to purchase them. You do get one hint to start each time playing. Words being 'weird' or 'uncommon': you can choose a dictionary of easy or standard. I find the words to be the same as any comparable game such as Text Twist or the anagram games of old.I like this game. I've had the free version and was happy to upgrade. It's easy to use the controls, and the words make me think.", #B004JKB83K
"Honestly, I have played games that were horrible. Many of us have I'm sure. And I'm sure the reviewers that only come on for the fact that it's free and give the app only 5 minutes before they review it would agree (if they actually kinda gave it a little more time) it can really work your head.Yeah it's not the best version ever. I think what it really is it is definitely a low grade software for a really high grade price. 5 bucks is outrageous for such a simple game. I think this would be catchy if it was completely free, but still 4 stars at most even of it was such.Come on Devs. You're selling a not very addicting game for an absurd price. It's very basic in every single way and felt like you're playing an old school preinstalled Nokia game with a bigger screen. Uninstalled.", #B004JKBPJ2
"Word Mix lite :  mind stimulating entertaining  This and app is on the top of my list. I love it!", #B004JKCMGM
"This app is not for me. Maybe for the younger people it will be great. I guess it depends on the age.", #B004JKCQUY
"this game is great.  it is because when I was little I couldn't get enough of it .now im grown. and its even better", #B004JKF21Y
"I didn't get to play it because it would not conform to my tablet's screen size, 7 inches.  Maybe it will work better on a cell phone.  Because it was so small, my tablet would not let me play it so I uninstalled it.", #B004JKHT4C
"This is a fun game!  The other positive reviews are right on about this game.My hubby had a stroke and this game helps him too. Give it a try!", #B004JKJ544
"This app fully performs the function stated, and it does it well. It's a practice slate for writing your letters, with an optional drawing guide that shows you how to trace it.The one thing I miss from the actual paper ones is the numbered steps and arrows. This just has the dotted letter outline, no guide around it.And some of the letters look weird, but that's probably either a font choice, or copied from a different brand of schooling material than I used way back in the day. Doesn't harm the app any.Overall, pretty good.", #B004JKJCTW
"Satisfies its title and description. 4 stars given for the ads in the &quot;pro&quot; version. Pro should be ad-free. Otherwise, perfect implementation of a bubble shooter.Will be playing for a while.", #B004JKJH1A
"This will entertain the kids and yourself for a while. Works well on pics with good lighting and good frontal view of one person. Also worked great on HTC evo.", #B004JKKJZS
"This app really helped me prepare for what turned out to be quite challenging interviews.  The question content was right on, and the rehearsal mode is just perfect for getting in the groove just before interviews.  I especially liked the Random Ordering mode to keep me on my toes.", #B004JKKXBI
"I always wanted a easy way to find Allah's name. This one along with its explanation is letting me do that. I loved the app a lot.", #B004JKKZNO
"1. Not HD AT ALL;2. 'Auto Pilot' put my boat into REVERSE;3. Controls are WAY too sensitive;4. The developers could've at least added decent audio.", #B004JKL3SU
"I always wanted a easy way to find Allah's name. This one along with its explanation is letting me do that. I loved the app a lot.", #B004JKKZNO
"bad bad very bad, who the hell wants something like thisPlease refund any money I might have wasted on this stupid piece of crap app", #B004JKOOHC
"This is a pretty basic version--I like that it provides audible tones to indicate when to transition from walking to running and back. I didn't use my phone's MP3 player & kept glancing at the phone when I thought enough time had passed for transitions the first two times I took it out. Not many fancy bells and whistles, but a nice, basic timing app that got me into running again.", #B004JKOYGS
"This is a new game for me.  Never played anything like it.  Very challenging.  Its like chess meets tic tac toe.", #B004JKQF3S
"Seems like a great idea and something my granddaughter would like but it is buggy and doesnt work very well.", #B004JKQIOY
"SSeems helpful to warn about apps misbehaving. Not obnoxious like other app killers who warn about all apps who only reopen after killing. This app seem a bit more intuitive though I'm am not sure about its effectiveness.", #B004JKQP92
"Works great on my phone. Completely unplayable on my Galaxy Tab.  Hopefully they will release an HD verson. (this is just fill in character because it require a minimum on 25 to write a review)," #B004JKRZNM
"Not much to say, really. Straightforward app that does what it's supposed to. Using it on 3 devices:* Asus Transformer TF300T tablet* Google Nexus 7 LTE (2013)* HTC Evo 4G", #B004JKTDRI
"The news is outdated and the site is not kept current. If they kept the site maintained I'd read it every day.", #B004JKTYOA
"Obama and Me? More like Obama and Wheee! Impress friends, family and coworkers with your collection of pictures with the President. He'll class up any photo album.", #B004JKU21O
"Very interesting app. I sent a few pics myself but have not seen them 'appear' on the app screen. Very diverse group of pictures.", #B004JKVFZG
"This is a useful, versatile tool for tracking exercise. I use it for everything from serious workouts to meandering explorations with a 4-year-old.A couple of suggestions for improvements:I was unable to retrieve data I uploaded to the server. I don't know whether  I set or did something wrong or what; I haven't tried thet again.I wish it were easier to update my weight, since I'm using this as part of a weight-loss program (and it's working!,)." #B004JKVM5E
"the title says it all della fantasma. it free. free free free free free free free free free free free", #B004JKYZQ2
"I subscribe to Popular Science and thought this would be a nice diversion for reading 'on the road'. Alas, it didn't work on my tablet with Android 4.01 (Ice Cream Sandwich). ;&lt{" #B004JL3JTA,
"Why does an app need 2 read your contact data. I would avoid all apps from this new data mining publisher that's pretending to be a game maker. Shut them down now and teach all app companies that data mining isn't acceptable.", #B004JL5BQ4
"Remember when Frostwire ONLY did MP3's? Doing torrent s now give you a wider and better search results. Its my go to when all else fails.", #B004JOSUMI
"Pretty good the only problems  have with it is that when i want to do a cover it most likely says something like: Couldn't get a pic or no results but i wouldn't say it's bad app.", #B004JOV0Z2
"As an avid user of of Flickr online and on my AppleTV2 I love seeing slideshows of recent events that I have taken pictures of, so it seemed like a great idea for an app. However, after downloading the app and trying to install it, nothing happens. I can't uninstall and I can get it to open either. Disappointment.", #B004JOVXFE
"This app is simple yet awesome!  Streaming music and lots of info readily available.  A MUST DOWNLOAD FOR CLASSICAL MUSIC LOVERS!!!!", #B004JOW8PI
"The program is fine, but nothing amazing. The permissions are steep, and all of those saying it's necessary are full of it. I have 3 similar apps on my phone and none require all these permissions. It's either poorly developed or taking advantage of you. Real shame is amazon refuses to tell you permissions before you download, which means your stuck hearing peoples opinions about permissions rather than reviews about features.", #B004JOXGPO
"I apparently accifently bought this useless app. Installed OK. but why 3 separate icons? And it runs as a widget. I live in Korea and don't drive. Since NO speeds for my town seem to be in here. it's a good thing I don't rely on it. That is the one time it ran for long enough to check it out before it crashed again. It locked up my phone once and crashes every time I run it. NOT even close to ready for prime time.  Galaxy S", #B004JOZJBI
"If there are instructions I haven't found them. Each hand is a stand along, which is good if you are a beginner but it needs a full game mode to serve my needs.", #B004JP0AFW
"This is a very simple app.  It is a timer that will NAG you into doing whatever it is timing.  You can set the alarm to loud and continuous, and it is impossible to ignore.  I've had it for 3 phones, and it is one of the first apps I re-download when I upgrade my phone.  I personally use it for the waterer on the garden.  If I don't set a timer, I end up with a lake.  I've tried other timers that ding, but one ding doesn't seem to make enough impression on me.  It is absolutely necessary for my life management.", #B004JP235W
"This is a really cool app, I know it was written for a cell phone but I used it on my Motorola Xoom.  I am still playing with the settings but as well as it worked I went and bought the full version that gives you all 20+ effects.  Well worth the money and once I finish understanding the best way to use it on the Xoom this will get a 6.", #B004JP35YA
"Has a box to type a word to search for but after pressing the search button  a message is displayed that it is 'Retrieving Content'. No content is ever displayed. I tried removing it from my Kindle and then pulling it off of the cloud to see if that might help but it didn't. Luckily it was free.", #B004JP365I
"Great app and service.  I really like the pay as you go service.  They also have a broad range of OS support so it works on my other non-kind devices.  I've used everything out there you can imagine (Onenote, everyone, smart receipts, neat, etc....) and this was the best and most feature rich.", #B004JP3ZJK
"Indeed is your all-in-one job search site.  You can post resumes, profiles, and it searches for you the other places like CareerBuilder.  Only search engine I would use."] #B004JP482I

more_non_sarcastic_text=["This game was fun to play but was not as good as 1 & 2. I would still highly recommend it.",
"Very addicting!!!",
"People have been asking for this game for a long time it's Amazing you get to unlock new fur coats",
"I love this game it is sooo AWSOME!!!  Get it it is rockin AWSOME!!!!!!!!!!! It's kinda like WoltQuest only your a fox. Get it!",
"Could not get this app to open.",
"Couldn't get it to work on this cheap Chinese Android",
"There are some really realistic laughs in this app. I've been having fun with this for the last few days pranking my friends and family! I recommend it.",
"There's some nice cry sounds in this app. They seem realistic for pranking. I will definately use this in the future. Thanks for your work!",
"Love &#60;3 &#60;3 &#60;3 &#60;3 !",
"Using this keyboard for couple of days, it's really intuitive & fun to use.",
"It's good",
"I like it very much",
"This was the worse slot game I've ever played. It took over 20 spins before I won any $$$. Downloaded and deleted within a hour!",
"Really fun game! Addicting too, keeps you guessing!The noise from the doors makes you jump though, loudest noises in the game so far.",
"this game is fun but kind of hard to pick up some of the items. this game is a fun game to play at night if u have nothing else to do.",
"Awesome. Really good real world physics. Really good fun and challenging.",
"This is a Fun and cool 3D Airplane game! Love the 3D graphics and its fun to play. I would recommend this game to everyone that loves simulation games!!",
"Love this game!!!!! All the scenes are sooo pretty!!!! 10 STARS",
"Another great hidden object game from tamalaki.  We snatched up almost all of them at the sale prices.  Tons of different ways to play this game!",
"Addictive and also the only woodchopping game on amazon I have found with 8-bit graphics.",
"Whilst playing this game I was enthralled at the wonderful features to which make this game unique. One feature I find prominently enticing is the 8 bit graphics.",
"Great summer themed puzzle game.  Lots of beautiful images of mountains, waterfalls and the beach.  Lots of fun!",
"NOT WORTH BUYING you pay for it then you have to invest more money or wait to be recharged to continue",
"Beautiful graphics and smooth animation. I'm so addicted to this game that I kept playing again and again.",
"This is an excellent game. The candy land setting is great and I have ready played through the first 10 levels without a break. Give it a try.",
"At first when i saw this i thought it was going to be ANOTHER flappy bird remix, but when i started playing, it turned out to be an amusing fun game!!",
"This game is so ADDICTING and I can't get tired of this game. When I play this the first time I was so surprised that they made this and I never get tired of it so you guys should play this game. You will regret it!",
"Love the Fix My Car series, but this one was my favorite.  Only wish I could see more of the girl :)  Cheers.",
"Really enjoying this one, played the other Fix My Car games too.  Game brings you to paint job, then you need to upgrade to full.  Upgrading.  Thanks guys.  Just wish there was more of the girl!",
"Pretty nice graphics, funny characters.Good choice for preschool kidz!Good Job! Keep it up!Looking forward for the other products of the developer!",
"I really love this kind of game it gets me thinking just to solve the pica.Thank you for providing this great games for us and I love that they are free.",
"Nice app. does the job pretty well. just the app I was looking for to do the editing on the go. highly recommended",
"Simple yet lovely design. Creative game play. It's definitely an addictive puzzle game.",
"what a smashing game would recommend it",
"There's not much not to like. The environment is well drawn and the game itself is well thought out. Recommended way to pass time.",
"This is an awesome counter! It does everything you need a life point counter to do but the best part is the custom background. Any picture you have saved can be made the backdrop....sweetness.",
"Love this game graphics are great just want them to make were you can have two loadouts during a hunt",
"This is the best game ever but if they could add mulitplayer it would be even better but still it Is very Awesome get It NOW",
"Absolutely wonderful!! One of my favorite games ever. So many neat and cool puzzles",
"Good game, just the right level of challenge that also allows you zone out and not get stressed.  Highly recommend for those who want a combination of jigsaw puzzle and hidden object.",
"The product description clearly states minimum operating system is android 2.2 (froyo), but you have the app as showing imcompatibility from Amazon (red x's) with the device I purchased it for!  Either fix this or make up your minds as to what devices this will run on AND that it can be downloaded for!  Sheesh!",
"This game is fun for little ones. It teaches the numbers and the alphabet in fun little activities. And when you pass a level you get prizes  like coin codes for doodle club",
"I love all of the cute pets:). My favorite is the monkey. There's so many games to play. Get this game! It's great!!",
"It's a really nice and fun game its good for 4 year olds I love it so I think  thell LOVE it  toI hope they like it it's really fun.  LOVE.  U  by peace out",
"Omg I play as a cat its sooo cool!!! I love jumping on people and throwing stuff from shelves! Best game ever!",
"This works great with beautiful artwork and the the text from the angel card reading is OUTSTANDING! Much more in-depth than some of the other apps like this. Highly recommend.",
"This game I don't like",
"This up is  free in amazon and after installing it  i found  helpful  finance info in it,to all persons this app is very free and easy to download.this will help you build the future ahead.",
"i have just downloaded it on my i phone ,its exactly what i was looking for  it has a very detailed information on how to manage and budget for what you have.a very powerful app on amazon.",
"Addictive and fantastic game for kids and adults alike! Hurdle jump is our favorite with the Yeti character, and best of all, the power ups are free, so we can add more in whenever!",
"Very fun game for both the adults & kids.  My daughter & I love playing the Hurdle game especially but the jump rope one is super fun too!  So fun watching your character lose the fat.  Hours of fun & I highly recommend!",
"One of the best pixel-style games out there! Super simple to learn yet nearly impossible to master!",
"This is so fun and addictive - can't put it down.  My whole family is fighting over who gets the Kindle next to play Balance of the Shaolin!",
"Whoever you are &amp;#34;ruby slippers&amp;#34; your not telling the truth about this game! It's not bad at all. It is a great challenge! It helps pass the time when you need it. It's addicting!!!!",
"Noone should play this game! I don't even know why this game was even created and put in this world",
"I like this game because it does not take up much storage space and whenever I am bored it is a simple game I can play to pass time.",
"It's really good very simple and easy to get the game and very good to pass time",
"I think it's lame that you get 20 tries to start and then you only get 5 there for after and it is dumb the fat re sets every 2 hours.....how would you ever win",
"This game shows different ways to stay fit and lose weight and at the same time having fun. This game is amazing and very addicting",
"Such a cute and fun game and more importantly very fun to play !",
"These are really great scenes in and around Beijing. The objects and add-ins are a bit cartoonish but overall if was an enjoyable game.",
"If you hate flappy bird Crush Bird is a game for you, I hate flappy bird and every time I kill a bird I feel great thank you levgenii Mykhalevskyi.",
"This game is very easy and fun.Flappy Bird is impossible and boring.If you have a sense of good games you would play this and give it a 5-star rating.",
"Wow what a waste of time man! I wish People would QUIT DOING THIS CRAP!! Its just a waste DO NOT GET IT!!HOW CAN AMAZON EVEN ALOW THIS IN THE APPSTOREITS JUST FILLED WITH ADDS, ITS NOT EVEN A GAME!people that do this crap just nee  to SCREW OFF!!!!",
"Truly inspiring and exciting game! I'll recommend it to all my friends! Super cool!You must give it a try for certain. You won't regret, I promise",
"It's stupid because u can't make the blocks straight and and its when u move around u can't really move your head but the graphic are ok",
"Could someone tell me how a person is supposed to play these games from FGL without matches and about s fourth of the playing field hidden???? I'm at a loss.",
"I was so very excited to see a new Hidden Garden Hidden Object game.  I immediately bought a bunch of amazon coins so I could buy this one and others if available (where are the other new ones? You usually release several at once).  Anyway, I don't know how they did it but this app is a little different than usual.  When you find an object it kind of pops as it disappears.  There's also a little pointer to show where you pointed.  The colors are richer and the pictures more beautiful.  The objects are also just a little bit harder to find which is wonderful because some of the other apps were too easy.  These aren't so hard it makes the app frustrating.  All in all, this app is awesome.  Welcome back Hidden Garden, we've really missed you!!!",
"I like it.",
"Love this game! Such a great summery feel! Can't wait for the other seasons and holidays to come so these guys can create some great games!",
"Amazing images!  I love gardens and these are beautiful! Lots of game modes different ways to find the items.  The second round had me finding different items then the first.",
"Kept me mesmerized since I have burned out other games that are like this.",
"Fun and challenging.",
"I Love it :)Some good to know info and tips.worth the time and the download",
"Good app,realy valuable tips, and definitly going to save me some money soon.Basic app, but gives you some added value.Hope I helped...",
"Well worth having.  Makes for a nice pocket oscilloscope AND does FFT Spectrum analysis in REAL TIME.Get it while you can.",
"The idea is good but I can make the app work in my Kindle.",
"This app makes picture taking fun.",
"I like this game very much. Simple challenging yet addictive. I also lik r doing their save bubblee witch saga game",
"it is a pretty adicting game. I like almost everything about it.the only thing is it glitches up on me sometimes but it might just be because of my kindle fire.I like that on my kindle its a little bit bigger and that's easier.",
"it doesn't work it starts up but then it says &quot;the game has stooped unexpectedly&quot; so if you can get it to work I'm sure its a good game ,but it just doesn't work for my kindle fire :( if it did work for me I'm sure I would like it.",
"This game is absolutely awful!!!!  The only thing it has is cute pictures.  Whoever thought of putting this out should be ashamed.  I know I would be.  Do not waste your time on this ....This....hmmmm...so bad I can't think of a word to use....lemon?",
"This app is fun but,made for beginners to the German languge.It is also limited and didn't take long to go through all of examples. Let me know when you make an app that is more challenging and made for advanced to intermediate people who study Deutsch and wants to keep there language skills advancing when they are not in Deutschland.Danke",
"Very cool presets to work with good price ive bought both essential preset packs and i love them very great to make music with i love gstomper it rocks making industrial music is my hobby so its pretty fun to make full songs bravo gstomper you make the best app in the world",
"I love this its a simple 8 bit music maker it makes me feel like a pro great job keep up the good work :D",
"I like it but controls are tricky but I would recommend it as a good game but it can't beat mine craft or survival craft",
"I'd rather get Minecraft. I already have it though. Nobody can beat it. This is not bad though. It's a cheaper version of Minecraft but still not as good. :)Minecraft 4ever.",
"I love this game! You have three classes to choose from. Warrior, Mage, and Hunter. But before you play you have to sign in to Face Book or Ngames. But you can register for Ngames it is completely free. The graphics are really good. So is the gameplay. If anyone is looking for a good rpg then I highly recommend this game.",
"The game is currently in an Alpha testing stage at the moment so it wouldn't be fair to make final judgements just yet. As for gameplay and mechanics its really simple. In order to play you'll need to sign into facebook or sign up for an account provided by the devs, free of course. First off you chose your class. Warrior, Mage, or Hunter. The game isn't gender locked so you can pick whichever gender you please. You simply do &amp;#34;dungeons&amp;#34; to earn experience and complete quest to earn additional experience.Your party for dungeons consist of 5 characters: Your main hero and 4 assistants. The game is an MMO but you can only interact to players by: Chat, PvP arena, Guild battle, Scramble, Town hub, World bosses.As for fighting mechanics it's auto battle style. You watch as your party fights against the opposing force, be that players or AI. The game is only in Alpha so the game might be a bit buggy, but thats the purpose of the Alpha, to find bugs and report them to the devs so it can be fixed.I gave the game a 4 star rating because of the in app purchase method. When you perform in app purchases you have to put in your mobile phone nunber and then follow instructions given from there and when your transaction is completed you'll be charged on your phone bill. I think this is a bad method seeing that I have a credit card linked to my account and cant use it to make a purchase. I hope the game will support in app purchases from the app store instead of the current method",
"It is annoying how you move so slowly and I really wish you could fly like in mincraft p.e.  It has room for improvement.",
"THIS IS THE WORST GAME EVER NOBODY SHOULD EVER GET IT YOU MOVE SO SLOWLEY CANT FLY AND THINKS ITS LIKE MINCRAFT IMA GAMER GIRL SO I KNOW THESE THINGS I RECOMMEND REAL MINECRAFT NOT THIS STUPID STUFF.",
"No rhyme nor reason to game! Plus there are no understandable directions",
"I have no idea how to play this and there are no directions.",
"Luv it luv it luv it",
"Super cool game",
"To cool. Literally! Lol. So anyway I was Board and wanted to get a good fun game, and I found what I was looking for.:-):-)&lt;3",
"It kinds skips on me but its kinda fun.I like it. Hope you do. pretty good. not much there though.",
"its kinda weird it has toe rings that all.I have to say. but has to have 20 words minimum soi wrote that",
"Help me sometimes to keep self reminders ... Now I can schedule a message and do my work . The app also has the feature to send immedite texts. So I don't need to switch between apps",
"Very enjoyable. I recommend it for those who love to battle, and action. A game that all ages will love.",
"This is a great game. You can collect weapons battle other players and much more! In the beginning you can choose which class you want to be. There are four classes total, Knight, Berserker, Mage, and Pirate, I'm all four! Plenty of dungeons to play in, or campaign, and almost always a match on multiplayer mode. I hope you have a great time playing!~ Kid",
"Excellent",
"good app for coverage of the open championship.  scores are updated almost immediately and coverage of other tournament news is thorough.",
"I love amazon",
"Really hard to control the plane.",
"Too fast",
"Simple and nice game, both for kids and adults.",
"it is a good and really fun app because you get to awnser the blank partand that is why I like the app",
"Just downloaded this app for my Android device and it's awesome! Can't wait to use it on my upcoming trip to New York. This seems like a really interesting way to learn the city and its history!",
"Just alright,  color would help ,it's not real hard  Good way to kill time.",
"If you are familiar with Cubistry, the game that precedes this one you will love this one too...but this one is very different. Rather than having brightly colored cubes, this game has a monochrome color-scheme with several shades of obe color. The symbols are harder, but that only adds to the challenge. It took me about 6 games to get use to the symbols. Love it.",
"Anything written by Joel and Victoria is inspiring and directional. I am touched by their sincerity and devotion.",
"This is a very inspiring read. Anything with The Olsteens will be motivating, inspiring, and a great read.",
"This is a very detailed simulation (you even have moving objects like the rotors of a wind farm).There are six different areas, though they are rather similar.You can choose either an old glider like Otto Lilienthal flew, or a sailplane.Goal is staying aloft as long as possible and reaching the highest possible altitude.To do this, look for updrafts, these are hazy cylindrical columns.Don't worry if it says warning, updrafts is what you need.Avoid columns with solid blue stripes, these are areas of strong turbulence that can damage and even destroy your glider.The only minor issue I have is on Kindle Fire HD, the framerate is visibly low which leads to slightly laggy controls.Still, a solid five.",
"Great app, makes learning about the Moon lots of fun. Had a great time trying all the different colors styles. Check it out.",
"This is a fabulous little app to explore the surface of the moon and the technical support if you need it is first class.",
"I love it!",
"I'm so addicted download now.",
"I really really like this game!",
"It kept freezing so you never got to do anything I deleted it right after I got it",
"This is the second one today. Why in the world do people do this. It's some .....! uhgggggggggg'  A advertising scam. I'm sure there will be a third, the other is Baris zombie hunter .",
"This app requires a LOT of information about your location,network, apps used,etc which is irrelevant to finding your pets age! This is more like spyware, I would NOT recommend it to anyone or even download it!",
"LOVE THIS APP! Helps me save tons when I'm out shopping!",
"Great to have coupons from all your favorite stores at your fingertips!",
"First time playing 2048 game now I understand the hype. It's very fun!",
"I have searched several 2048 games before i found thid one.This one is the best.You have different kinds of choices.Love this game.",
"I use it daily to track my spending. Helped me save a lot since I started using it",
"Great app! Love that it highlights possibly fraudulent transactions and helps me easily investigate. Great interface and design, highly recommend!",
"In all honesty this game and this series is a complete work of art each of the books come and work together beautifully  when I saw this book came out I literally thought I was gonna burst with joy hero rose gets a big thumbs up from me and I would recommend this book to anyone who loves a story that captures your imagination",
"This game seems good... but can just be one big disappointment depending on the choices you make.1) in order to kill Victon you have to have a high revenge level. Your revenge level can not be 60 (it probably has to be around 75) or below otherwise you can't kill him.2) towards the beginning of the game it gives you an option to choose that suggests you have romantic interests in Prodigal but you can't actually have a romance with her.3) you get the option to unleash your powers with reckless abandon close to the end of the game but you have to have a high unleash level otherwise you can't unleash your powers.4) *****Spoiler Alert*****you can't save Prodigal in the end***********************************5) you would think that some of the characters in the game would have an indicator to show how they feel about you. I know a few do but characters from the last one are in here and most of them don't. *******Spoiler Alert********Like GG and the crush, for example, do not have one.*******************************************6) this heroes rise seems a lot shorter than the last one",
"I would totally give it 5 stars but it keeps randomly crashing in my Note 3. Great gameplay, music and story, love it.",
"Fun and addicting RPG. I like where this game is going and hope there will be updates. Just be aware of crashes.",
"I own this game on my kindle and PC.  I feel the kindle version of the game is easier.  The company that sells Hobby Farm Show asks for reviews so the sequel can be developed.  What I do not understand is why they need the reviews the sequel is available on the PC.  If you enjoy time management games you will enjoy this one.  The only thing you have to buy is the rest of the levels.",
"Great for younger kids they are learning that you have to take care of crops and the animalsThey are so fast",
"This is an easy way to see if you like the game, since it's free.  I purchased the full version after trying it since it contains more challenging puzzles, which are also worth more points.  Both versions are integrated with Amazon's GameCircle so you can post your score to a leaderboard and see how you compare with others.",
"So challenging and fun for ages of all. Wish could play them on Facebook and share with my friends  hope u guys add to Facebook soon",
"Downloaded this game for our new Kindle, but quickly took off the app. The only game that we enjoyed was the car racing, so we deleted this app and looked for others. Sorry - not what we were expecting!",
"I wanted to try this app since this developer has put out some interesting games. However, I am unable to download it as it says there is a geographical restriction.?? This made very little sense and I called Amazon customer service, which was a HUGE waste of time. They didn't seem to know what was going on.PLEASE fix this app so it can be downloaded....",
"not bad",
"An addictive little gem of a game. Basically letters fall from the sky and you have to make a well known inspirational or motivational Bible verse. It's not as difficult as it sounds as many of the letters are already filled in for you. I usually start with the smallest words first. GREAT FUN! FIVE STARS!",
"The Best",
"Normally Noodlecake Studios puts out pretty good games. This is not one of those. It is too difficult, too hard to understand. I am a very intelligent 31 year old female who likes interesting and difficult strategy/puzzle games. This one doesn't even make much sense. I would love my money refunded but I highly doubt that will happen.",
"First review :D, anyways this game is like super hexagon. It is super hard, it can will change from spinning to tilting, and it might cause seizures. don't get this game if you don't want to be over challenged or lack focus, otherwise knock yourself out and good luck, you'll need it",
"Really good fun. Pretty challenging. Even better than the last one.",
"Names don't fit on stones",
"Really fun game. Some tricky little shots in there to be found.",
"Awesome game, beautiful scenes and objects are super tiny and impossible to see to the point where you get upset.",
"They are all interesting ...wish they had more levels",
"It was a good game but some major issues that need to be fixed. If they fix the problems I will definitely change my review but it kept kicking me out of the game... not sure if it is just on my device but... hope this helped you :)",
"I liked the game but every time I  went to the main screen it would crash.  Once they fix that, I will  be willing to give this a better rating",
"This game is awesome. Great time killer. Never gets old. All in all I'd have to say... AWESOME!!",
"unable to connect ot anything",
"Life is a game, Baseball is serious.",
"Perfect - now need to get NFL Sunday Ticket and NHLCenterIce",
"GOD BLESS, YOU AND COMPANY",
"Arcade like old school feel",
"Superb and Addictive",
"Not much there - picture not crisp and clear",
"Only wish I found this app sooner!",
"The objects you are trying to find are so small that I have a headache from squinting. It is also very short. 10 scenes and end game. To be fair after each HO scene there is a find the differences screen and then you look for a golden key on an additional screen. They are both like the HO scenes. It is definitely a traditional HO game, so if you like straight HO with no storyline then the concept will appeal to you. Be forewarned about the tiny objects, however. If you do find them, take care in your aim because you lose points if you hit them even a bit off.",
"Best dad ever",
"i love hockey",
"Really good. Almost there. All this app really needs is a section where people can add a comment. Still, it is better than the other Youtube apps out there. I recommend",
"I had been looking for a way to watch YouTube videos on my Kindle when a friend told me about this app. Other apps I found as &#34;workarounds&#34; were hit or miss. Now I can enjoy music and videos on the go",
"A fabulous looking app with a lot of potential in the future. (It's a mobile site wrapper atm)",
"good game",
"Cost: for me it was 99 amazon coins or $.99 cents.Download size:32.6 mb.Install: When installing this game it gets access to:Privacy:a - read phone and identityb - modify or delete the contents of your USB storageread the contents of your USB storagec - find accounts on the deviceDevice Accessa - full network access.b - view network connections.c - view Wi-Fi connections.d - runs at startup.====================================================The game is published by Tamalaki. http://tamalaki.com/whois.htmlWho is Tamalaki?  -- Tamalaki is founded by casual and online gaming expert Martine Spaans. In previous roles she has led the Game Licensing department for Spil Games and rolled out the Online Marketing strategy for companies like Ubisoft/Blue Byte and Gramble on both Web and Mobile. She&#8217;s looking forward to use all this experience to bring your games to the right audience and to give them maximum exposure. Martine is also offering her expertise as a consultancy service. Feel free to get in touch if you&#8217;d like to learn more.",
"This is the best skateboarding game on the market.  The graphics are amazing, the controls are great, the tricks look SO REAL and the levels are awesome!  Rooftops is my favorite level...HUGE gaps and tons of air!  Way to go Transworld!",
"I really love the new version because they added missions and career modes for the skaters. My favorite skater is Danny Way.  Highly recommend!",
"Quite a simple flight plan that became a family challenge of outscoring each other.  Our 6 year old loved beating gramma !",
"I Use to play this game with my dad when I was a kid all the time it's hard to get anyone to play it any more. OMG is exactly what I said when I saw this game and I don't mind the adds because you get extra coins in the game for them.",
"This app is so amazing and I actually did not think that the app would work so well, buy this app it's awesome!-Brianna K",
"This is a good game for people who have plenty of time to waste. However, all you do is simply press buttons. It gets very boring after awhile, and I think should be preferred to children. The ads do get frustrating too, and I think that should be improved as well. I do NOT recommend this game.",
]

non_sarcastic_text=non_sarcastic_text+more_non_sarcastic_text

print("LEN NONSARCASTIC TRAIN: "+str(len(non_sarcastic_text)))


import csv
with open('MTurkData_for_Model.csv', 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
	for row in csvreader:
		sarcastic_text.append(row['Text'].decode('unicode_escape').encode('ascii','ignore'))

print("LEN SARCASTIC TEST: "+str(len(sarcastic_text)))

"""
Install Instructions
pip install textblob
python -m nltk.downloader
sudo pip install -U nltk

"""

"""
Sentiment pattern
Will extract a sentiment pattern from a string of words.
The pattern can look like many things as dictated by the options.
The default options result in a pattern simmilar to (-1,1,1,1,0 )
"""
def sentiment_pattern(text, gram_n=9, predictor=None):
	
	blob= TextBlob(text)
	ngrams=blob.ngrams(n=gram_n)
	sentiment_list=[]
	datalist = []
	for gram in ngrams:
		str_gram=" ".join(gram)
		data = (0, 0, str_gram, None)
		datalist.append(Datapoint(*data))

	if len(datalist)==0:
		return []
	else:
		prediction = predictor.predict(datalist)

		for sentiment in prediction:
			sentiment = int(sentiment)
			if sentiment < 2: sentiment = -1
			if sentiment == 2: sentiment = 0
			if sentiment > 2: sentiment = 1
			
			sentiment_list.append(sentiment)

		return sentiment_list
	"""
	blob= TextBlob(text)
	ngrams=blob.ngrams(n=gram_n)
	sentiment_list=[]
	for gram in ngrams:
		str_gram=" ".join(gram)
		gram_blob=TextBlob(str_gram)
		sentiment=gram_blob.sentiment[0]
		if sentiment>0:
			sentiment=1
		elif sentiment<0:
			sentiment=-1
		sentiment_list.append(sentiment)

	return sentiment_list
	"""

def crush(pattern):
	if pattern==[]:
		return []
	else:
		last=pattern[0]
		crushed=[last]
		i=1
		while i<len(pattern):
			if pattern[i]!=last:
				crushed.append(pattern[i])
				last=pattern[i]
			i+=1
		return crushed

def neutral_exclude(pattern):
	return filter(lambda x: x !=0,pattern)

def check_cue_words(text):
	CUES=[
		"stupid",
		"shit",
		"oh",
		"yeah",
		"sure",
		"forget",
		"supposed",
		"dont waste your",
		"all of my",
		"go back to",
		"a pair of",
		"needless to say",
		"are looking",
		"!",
		"..." 
	]
	return any(imap(text.lower().__contains__, CUES))

def speech_patterns(text):
	blob = TextBlob(text)
	tags=blob.tags
	if len(tags) == 0: return []
	ngram, tags = zip(*tags)
	tags_gram = zip(tags[:-1], tags[1:])
	

	return tags_gram


def make_test_data():
	#Both of these peices of data come from fillatova's corpus. We shouldn't have touched 
	#Load non sarcastic testing data
	non_sarcastic_test=[]
	path = './Regular'
	for filename in glob.glob(os.path.join(path, '*.txt')):
		review = ""
		start = 0
		for line in open(filename):
			l = line.strip('\n')
			if l == "</REVIEW>": break
			if start == 1:
				review += l
			if l == "<REVIEW>":
				start = 1
		if len(non_sarcastic_test)>=437:
			break
		non_sarcastic_test.append(review)


	#Load sarcastic testing data
	sarcastic_test=[]
	for line in open("sarcasm_lines.txt"):
		sarcastic_test.append(line.split("\t")[1])

	return non_sarcastic_test,sarcastic_test 

def extract_features(text, predictor = None):
	feature_dict_vector = []
	pattern=sentiment_pattern(text, predictor = predictor)


	pattern_tuples_list = zip(pattern, pattern[1:], pattern[2:])

	feature = {}
	for i in pattern_tuples_list:
		if i in feature:
			feature[i] += 1
		else:
			feature[i] = 1

	speech_tuples_list = speech_patterns(text)

	for i in speech_tuples_list:
		if i in feature:
			feature[i] += 1
		else:
			feature[i] = 1

	feature_dict_vector.append(feature)
	return feature_dict_vector

import dill
import pickle
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

tag_vector = []
tag_vector_test=[]
feature_dict_vector=[]
feature_dict_vector_test=[]
non_sarcastic_test,sarcastic_test =make_test_data()

print("LEN NONSARCASTIC TEST: "+str(len(non_sarcastic_test)))
print("LEN SARCASTIC TEST: "+str(len(sarcastic_test)))


print "Loading Predictor..."

predictor = pickle.load(open("predictor.pickle", "rb" ) )

print "Extracting Features - 1..."

for i in sarcastic_text:
	#feature_dict_vector+=extract_features(i, predictor)
	tag_vector.append(1)
	print sarcastic_text.index(i)

print "Extracting Features - 0..."

for i in non_sarcastic_text:
	#feature_dict_vector+=extract_features(i, predictor)
	tag_vector.append(0)
	print non_sarcastic_text.index(i)

print "Extracting Test Features - 1..."

for i in sarcastic_test:
	#feature_dict_vector_test+=extract_features(i, predictor)
	tag_vector_test.append(1)
	print sarcastic_test.index(i)


print "Extracting Test Features - 0..."

for i in non_sarcastic_test:
	feature_dict_vector_test+=extract_features(i, predictor)
	print len(feature_dict_vector_test)
	tag_vector_test.append(0)
	print non_sarcastic_test.index(i) + 1

#ONLY HAVE TO DO THIS ONCE-------------------------------------------------------------

# print "Translating Features..."

# vec = DictVectorizer()

# feature_vector = vec.fit_transform(feature_dict_vector).toarray()

# transformer = TfidfTransformer()

# transformer.fit(feature_vector)
# feature_vector = transformer.transform(feature_vector).toarray()

# pickle.dump(feature_vector, open("feature.pickle", "wb" ))


# print "Translating Test Features..."

# vec_test = DictVectorizer()

# feature_vector_test = vec.fit_transform(feature_dict_vector_test).toarray()

# transformer_test = TfidfTransformer()

# transformer_test.fit(feature_vector_test)
# feature_vector_test = transformer_test.transform(feature_vector_test).toarray()

# pickle.dump(feature_vector_test, open("feature_test.pickle", "wb" ))

#ONLY HAVE TO DO THIS ONCE-------------------------------------------------------------END


#ANALYSIS

# feature_vector = pickle.load(open("feature.pickle", "rb" ) )


# for i in sarcastic_text:
# 	tag_vector.append(1)

# for i in non_sarcastic_text:
# 	tag_vector.append(0)



# print "K-Fold Cross Validation..."

# TP = 0
# TN = 0
# FP = 0
# FN = 0

# for lp in range(0, 20):
# 	cv = KFold(len(feature_vector), shuffle = True)
# 	for trains, tests in cv:
# 		X1 = []
# 		Y1 = []
# 		X2 = []
# 		Y2 = []
# 		for i in trains:
# 			X1.append(feature_vector[i])
# 			Y1.append(tag_vector[i])
# 		for i in tests:
# 			X2.append(feature_vector[i])
# 			Y2.append(tag_vector[i])
# 		clf = RandomForestClassifier(n_estimators = 1000, n_jobs = -1)
# 		clf.fit(X1, Y1)
# 		Y_pred = clf.predict(X2)
# 		TP += len([i for i, j in zip(Y2, Y_pred) if i == 1 and j == 1])
# 		FP += len([i for i, j in zip(Y2, Y_pred) if i == 0 and j == 1])
# 		TN += len([i for i, j in zip(Y2, Y_pred) if i == 0 and j == 0])
# 		FN += len([i for i, j in zip(Y2, Y_pred) if i == 1 and j == 0])

# pre = TP / (TP + FP + 0.0)
# rec = TP / (TP + FN + 0.0)
# pacc = TP / (TP + FN + 0.0)
# nacc = TN / (TN + FP + 0.0)

# print "Sarcastic:" + str(TP + FN)
# print "Non-Sarcastic:" + str(TN + FP)
# print "Precision:" + str(pre)
# print "Recall:" + str(rec)
# print "Positive Accuracy:" + str(pacc)
# print "Negative Accuracy:" + str(nacc)

# print "F1 Score:" + str(2 * pre * rec / (pre + rec))


TP = 0
TN = 0
FP = 0
FN = 0

feature_vector = pickle.load(open("feature.pickle", "rb" ) )
feature_vector_test = pickle.load(open("feature_test.pickle", "rb" ) )

print len(tag_vector_test)

clf = RandomForestClassifier(n_estimators = 1000, n_jobs = -1)
clf.fit(feature_vector, tag_vector)

Y_pred = clf.predict(feature_vector_test)

TP += len([i for i, j in zip(tag_vector_test, Y_pred) if i == 1 and j == 1])
FP += len([i for i, j in zip(tag_vector_test, Y_pred) if i == 0 and j == 1])
TN += len([i for i, j in zip(tag_vector_test, Y_pred) if i == 0 and j == 0])
FN += len([i for i, j in zip(tag_vector_test, Y_pred) if i == 1 and j == 0])

pre = TP / (TP + FP + 0.0)
rec = TP / (TP + FN + 0.0)
pacc = TP / (TP + FN + 0.0)
nacc = TN / (TN + FP + 0.0)

print "Sarcastic:" + str(TP + FN)
print "Non-Sarcastic:" + str(TN + FP)
print "Precision:" + str(pre)
print "Recall:" + str(rec)
print "Positive Accuracy:" + str(pacc)
print "Negative Accuracy:" + str(nacc)

print "F1 Score:" + str(2 * pre * rec / (pre + rec))