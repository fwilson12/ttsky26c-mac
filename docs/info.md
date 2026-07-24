<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This ASIC is a single Multiply-Accumulator (MAC) module, which are the building blocks of AI accelerators. Although I could only fit a single MAC on my 1x1 tile, modern AI accelerators like Google's TPU structure their Matrix Multipliers (MXUs) with a grid of up to 256x256 of these MACS, which are called systolic arrays. These arrays are what make TPUs so good at deep learning computation; each MAC processing element stores a weight, and batched previous layer activation values are iteratively fed through the array, with each element calculating partial sums and allowing both the activation value and partial sum to continue to flow through the array, with each column of MACs corresponding to a single component's activation value in the next neuron layer (pre bias/softmax).

Due to the space constraints, I had to adapt the role of my MAC so it could still perform ML math; instead of receiving an activation from a neighboring PE and multiplying it by its stored weight, my MAC instead takes two vector components, multiplies them, and updates the running total that the accumulation reg stores. In practice, my lone MAC is performing the same task that an entire column of systolic MACs would; calculating the dot product of two vectors.

The pin constraints also left me with a tough design decision. While frontier AI accelerators deal with highly efficient fp16 values, at this small scale I've opted for signed int8s for each vector component. However, to get an accurate, live output, I needed a bit more than 8 bits of output. This led me to use all 8 bdir pins to stream the middle byte of a 24 bit accumulator register, and the dedicated 8 output pins for the low byte. To multiply two 8bit scalars with half the pins I need, however, I had to time-mux the vectors with a mini FSM with an internal reg that either stored the value from the pins, or multiplied the value at the pins with the value in the reg, depending on the state.

## How to test

Interleave two vectors, and stream the next value at each clock edge. The lower 16 bits current dot product partial sum will be exposed by { uio_out, uo_out }
