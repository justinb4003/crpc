# 3D printable Corsi-Rosenthal style box for PC fans

Some links to explain what a CR box is:

Here's a page featuring a lot of the original design: 
https://cleanaircrew.org/box-fan-filters/

Next is a showing that it works well with a 10" filter setup: https://www.texairfilters.com/a-mini-corsi-rosenthal-box-air-cleaner/

And then we get to the latest developmens where PC fans are showing to provide excellent air flow and remaining quiet:
https://covid19crowd.com/cr-boxes/

Devices like this are also used in wood shops to capture small particles. I thought I'd build a small one for home because I have chickens in my office right now (yes, seriously) and they kick up a bit of dust with the food and straw and what not.

![image](https://user-images.githubusercontent.com/16728804/213598181-c88eb7aa-8c2a-4248-a903-06b4e2bde62a.png)
*(A partially completed version. You can see the fan plate, corner plate, a 25mm wide plate, and a 120mm wide one on the bottom)*

![image](https://user-images.githubusercontent.com/16728804/213843588-e4caa7d7-2288-474f-bbc5-1ae52c98d07c.png)
*(A more completed box with 65mm corner plates, 121mm fan plate, and non-fan plate stretched to 120mm on the other three sides)*

## 3D printing the frame
There are 3 types of parts you need to print. A plate for holding each fan, which are sized at 121mm wide to give just a little bit of wiggle room for the fan to be out of spec with 120mm.  You'll also want to print some corner piece for the corners. A couple sizes are pre-generated for you. Last is the 'nofan' file which is a solid plate that is used to fill in between the corners and wherever you have a fan.

A quick and dirty way of doing is print the fan plate, print the corner plates of 25mm size, and a few 25mm nofan plates. You can then use tape to cover the holes left behind.

Or if you want it more solid, print the fan plates you need print the larger corner pieces, and use the nofan_plate_100mm and size it to whatever you need to. Being 100mm wide it's easy to figure out how to scale it. Need a 37mm section. That's 37% in the proper axis.

STEP files are also inluded so you can pull them into any CAD software and extrude it as you need.

Odds are the size of your bed means you'll need to print it in pieces. This would be a great one to run off on a belt printer.

The originals were geneated with CadQuery 2.0 (https://cadquery.readthedocs.io/en/latest/) with the code residing in ```grpc.py``` in this repository.

## Fans and Power

You'll want PC fans of the 120mm size for this. If you're unsure here's the set I purchased: https://smile.amazon.com/gp/product/B08R8M17S2 which have the 4 pin and 3 pin connectors. I can daisy-chain the 4 pin connectors together and apply power to one and they all fire up.

For a power supply I grabbed this: https://smile.amazon.com/gp/product/B071FNN9W7 which can output 1 amp of power. That is enough to run 4 of the above fans at max speed.

I left holes in the fan mounting plate for 4mm machine screws but 6/32 or 3mm will likely work fine. It's not a fussy operation.

So, for about $25, a bit of filament, and the cost of your filters and you're in business with a decent quality and nearly silent air filter.
