# aces-up

Script that deals new cards until they meet some conditions. Makes getting good scores easier in Aces Up - a card game from KDE's KPatience. The best possible score is 52-4+12=60 (clicking 52 cards minus 4 aces plus 12 deals). The more aces you have, the less moves (on average) you need to make. Also, if you have all starting cards in the same suit, you can discard 3 of them immediately. By default, the script terminates when 3 aces are drawn.

This script only works if you have:
* GNU+Linux with KDE
* Full HD resolution
* Maximized KPatience window
* Solver enabled in KPatience (Settings -> enable Solver)

To run the script just type `python3 aces_up.py` in your terminal and quickly switch to KPatience. There are 3 possible options you can use:
* For setting the number of aces you expect to have in your initial deal: `aces=<number-of-aces>`. E.g.:

```python3 aces_up.py aces=2```

* For getting all cards in the same suit: `suit`. E.g.:

```python3 aces_up.py suit```

* For setting the interval between deals: `interval=<time>` (default 1.6s because for 1.5s the solver once hasn't finished calculating the result for me). E.g.:

```python3 aces_up.py interval=1.2```

Probabilities
-------------

Here are the probabilities of getting a deal with the following criteria:

* 4 aces - <img src="https://render.githubusercontent.com/render/math?math=\frac{4 \cdot 3 \cdot 2 \cdot 1}{52 \cdot 51 \cdot 50 \cdot 49} = \frac{24}{6497400} \approx 0.00037 \%25">
* 3+ aces - <img src="https://render.githubusercontent.com/render/math?math=\frac{48 \cdot \binom{4}{1} \cdot 3 \cdot 2 %2B 24}{52 \cdot 51 \cdot 50 \cdot 49} = \frac{1176}{6497400} \approx 0.018 \%25">
* 2+ aces - <img src="https://render.githubusercontent.com/render/math?math=\frac{48 \cdot 47 \cdot \binom{4}{2} \cdot 4 \cdot 3 %2B 1176}{52 \cdot 51 \cdot 50 \cdot 49} = \frac{163608}{6497400} \approx 2.5 \%25">
* 1+ aces - <img src="https://render.githubusercontent.com/render/math?math=\frac{\binom{4}{1} \cdot 4 \cdot 48 \cdot 47 \cdot 46 %2B 163608}{52 \cdot 51 \cdot 50 \cdot 49} = \frac{1824024}{6497400} \approx 28 \%25">
* same suit - <img src="https://render.githubusercontent.com/render/math?math=\frac{13 \cdot 12 \cdot 11 \cdot 10 \cdot 4}{52 \cdot 51 \cdot 50 \cdot 49} = \frac{68640}{6497400} \approx 1.06 \%25">

Waiting times
-------------

Knowing the probabilities of good card sequences we can calculate how long we will have to wait for them to occur. Let's say we want to know how much we'll have to wait to be 95% sure we get the sequence we want. We can calculate it this way:

<img src="https://render.githubusercontent.com/render/math?math=1 - \left(\frac{all\_possible\_sequences-desired\_sequences}{all\_possible\_sequences}\right)^{number\_of\_deals} \ge 0.95">

...after some operations we'll get:

<img src="https://render.githubusercontent.com/render/math?math=number\_of\_deals \ge \log_{\frac{all\_possible\_sequences-desired\_sequences}{all\_possible\_sequences}} 0.05">

So after putting the numbers in and multiplying the number of deals by 2 seconds (as that's the interval between deals) we get these times:
* 4 aces - 811018 deals - 19 days
* 3+ aces - 16550 deals - 9 hours
* 2+ aces - 117 deals - 4 minutes
* 1+ aces - 9 deals - 18 seconds
* same suit - 282 deals - 9 minutes

You can decrease the number of seconds per deal by using the `interval` option.

How it works
------------

I extracted fragments of each possible card in a deck and calculated MD5 sums of these fragments. Then I hardcoded them in my script and it compares MD5 sums of dealt cards with the hardcoded ones. I used fragments of cards, because using whole ones is redundant.

I also compared all 3 possible Solver answers: "This game is winnable.", "This game cannot be won." and "Unable to determine if this game is winnable.". I then chosen a pixel that is different for the winnable text. Checked its RGB values for each text and created a condition that only uses green RGB value of that pixel (because it's enough). The pixel I chosen is marked red in this image (in the first text):

![solver_texts](https://user-images.githubusercontent.com/24587734/81459326-df8a7c80-918e-11ea-84f2-fbce83cc2c39.png)

So the script checks a pixel to see if the game is winnable. If it's not, it makes a new deal. There's no option to skip that check because in my opinion it's a waste of time to wait for a sequence only to later realise it couldn't be won.
