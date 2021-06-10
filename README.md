# Augmenting SNR Datasets through Advanced Learning Techniques

This project was developed as my bachelor's degree final thesis. Detailed information can be found in the pdf document.

# Table of Contents
* Technologies(#technologies)
* [Motivation](#motivation)
* [Data Collection](#data-collection)
* [Data Validation](#data-validation)
* [Data Generation](#data-generation)
* [Results](#results)
* [Further Steps](#further-steps)

# Technologies
* SRSLTE
* MGEN
* Python 3.8
* PyTorch

# Motivation
To satisfy the demands of 5G systems, there is a tendency to Network Functions Virtualization
(NFV) and Software Defined Networks (SDN). The integration of Artificial
Intelligence (AI) in this paradigms, such as C-RAN, will make use of Artificial Intelligence
techniques to make short time scale predictions of UE SNR levels, among other
channel state parameters. However, it can be challenging to properly train the AI models
without sufficiently large and representative datasets. This work analyzes how to
enlarge said datasets through advanced learning techniques, allowing an optimal analysis
of the SNR properties even when the available samples are much lower than the real
ones, eventually leading to more scalable algorithms.

It is also possible to extrapolate this work to other fields as the [Data Generation](#data-generation) part is general for any time series (with an appropriate hyperparameters tuning). 
# Data Collection
Retrieving data from a LTE base station is a rather trivial process in a real scenario,
but having access and permits to them is not that much. And even if they are accessible,
the data will correspond to multiple users and terminals, so keeping track of a particular
one is a costly procedure. 

Moreover, datasets of controlled metrics of individual users are scarce . Thus, for the
purpose of this project, original datasets are generated. The metrics of interest in this
datasets are the signal to noise ratio (SNR), the modulation coding scheme (MCS), the
decoding time, and the buffer state report (BSR).

## Devices and configuration
The available testbed for this study is based on the open source LTE library srsLTE,
which provides a fully working Software-Defined Radio User Equipment (srsUE), an eNodeB
(srsENB), and an Evolved Packet Core (srsEPC).

The testbed consists in two different Ubuntu 16.04.6 LTS devices, which, both have
srsLTE installed, and their network cards are connected by a RF cable. One of the devices
runs srsUE to work as a user’s terminal, and the other device runs both srsENB and
srsEPC to work as the rest of the LTE network. In this work the data is collected in the
second device as the scope of the study only covers the uplink parameters.

The request of the transmission gain modification is send by executing the script set_txgain.py. The open source software MGEN is used to generate traffic. It creates real time traffic
patterns that can be configured as desired, as later is broadly discussed.
Another tool used is iPerf, which utility is to measure the maximum bandwidth and
packet loss, among other parameters. It is therefore very useful to analyse the functioning
of the testbed.

## Testbed characterization
The crucial characteristics to understand the testbed behaviour for this work are the
maximum bandwidth and the performance of the signal to noise ratio at the receiver
with respect to the transmission gain set at the emitter.
Hence, this study only considers an uplink channel (and another downlink channel),
and a given distance between the UE and eNB antennas, it is possible that the measured
characteristics differ when this conditions change.

### Maximum Bandwidth
In order to know which is the maximum available bandwidth, the tool iPerf is used. The
procedure to achieve that goal consists in executing the srsue command in the computer
1, and the srsepc and srsenb commands (in two different consoles) in the computer 2.
After the UE is successfully attached and the connection is established, an iPerf UDP
server is ran in another console in the computer 2 and an iPerf UDP client is executed in
the computer 1. In the mentioned iPerf client, the bitrate is sequentially set to increasing
values every try. As the client bitrate increments, the received bitrate at the server
reaches a boundary of approximately 15 Mbps. This implies that when the client bitrate
is set to values above that boundary, the packet loss increases proportionally.

From that experience it is safe to say that the maximum achievable bandwidth is
around 15 Mbps, and that the packet loss due to bandwidth overflow is negligible if the
bitrate is set to values below 12 Mbps.

### Mean SNR with respect to the transmission gain
Both computers of the testbed (with their respective peripherals) are static and always
in similar conditions. Thus, for the signal to noise ratio (SNR) at the receiver to change,
the transmission gain at the srsUE device has to be modified.
In this case the transmission gain can be set in the srsUE configuration file as it
remains constant during the capturing periods, but by convenience it is set using the
Python code fixed_txgain.py before capturing.

## Capturing scenarios
The ground truth data has to be diverse enough so that it is possible to check that the
synthetic data can be generally valid. For that purpose, the real dataset is composed by
a combination of eight traffic patterns and nine transmission gain patterns.

### MGEN patterns
#### Poisson patterns
This pattern generates messages of a fixed sized and send them in a given interval that
varies following a Poisson distribution. In this work the packet size is set to the maximum
possible for UDP traffic: 8192 Bytes, and the sent packets per second is set to 31,
77, or 153, corresponding to 2 Mbps, 5 Mbps, or 10 Mbps, of uplink bitrate.

#### Burst patterns
As the name of this pattern announces, it generates bursts of messages of another kind
of MGEN pattern at a given average time interval. The distribution of this time interval
can also be chosen as exponential or uniform. The bursts last a time interval that can
also be chosen fixed or random. In this study the configuration used is: bursts appear
following a exponential distribution with mean 5 seconds, the pattern of the bursts is
a Poisson pattern with the same parameters explained in the previous point, and the
duration of the bursts follows a exponential distribution with average on 3 seconds.

#### Clone patterns
This pattern uses a tcpdump binary file and "clones" it, meaning that takes the packet
sizes and its correspondent timestamps from the tcpdump file and generates a traffic with
the same characteristics. In this work the tcpdump files are created using WinDump,
which is the equivalent of tcpdump for windows, capturing the traffic of video-calls
using two different applications: Skype and Hangouts.

### Transmission gain patterns
In a real scenario signal to noise levels may vary over time as the user terminal approximates
to the base station or as they get farther away, interference may also not
be stationary, or even the climatic conditions can effect. Hence, in this case the physical
conditions of the testbed cannot be changed to simulate these real scenarios, the
transmission gain is modified for that purpose.

The Python code used to modify the transmission gain following these patterns is in
the file set_txgain.py
#### Triangular waveform
This pattern tries to simulate the approaching and distancing of the UE and eNB. It
does so by following the form of a stepped triangular wave. The transmission gain is
initialized within the range of gain levels, and every 10 seconds the gain increases by
1dB, until it reaches the maximum level of the range, in which case, starts to decrease
by 1dB every 10 seconds, until it reaches the minimum value of the range. Then the
process repeats until it is manually stopped.

#### Random steps waveform
This pattern emulates the sudden appearance (or disappearance) of interferences. It
consists in, every 10 seconds, increasing the transmission gain by a integer value from
−5dB to 5dB that is generated randomly following a uniform distribution. If the new
transmission gain exceeds the upper or lower boundary of the range it is set to that
boundary.
#### Fixed gain
This simulates a more stationary scenario where the previously discussed conditions do
not have a mayor impact on the SNR, meaning that the transmission gain is set before
starting capturing, and remains at the same value until the end of it.

### Capture procedure
The capture procedure consists of 4 different steps:
1. Connect srsLTE
2. Set transmission gain
3. Send MGEN traffic
4. Monitoring

More details in the report.

# Data Validation
Before working with the dataset to generate synthetic data, it is crucial to determine
the possible correlation between the different parameters of the collected data as it can
facilitate the task by generating parameters together, or in the absence of this correlation
it can difficult the process.

In this case, the parameters of interest are mainly the signal to noise ratio (SNR), the
buffer status report (BSR), the modulation and coding scheme (MCS), and the decoding
time. These parameters are referred to the uplink, as are worthier of been synthetically
generated than been captured, in contrast with the downlink case.

Plots and descrpition of scenarios in the report.
# Data Generation
In this work, a Wasserstein generative adversarial network is used. It is formed by
a CNN generator and a CNN critic, due to the fact that these neural networks take into
consideration the time dependency between samples and the relationship between the
different input parameters. RNNs were also tested, as they also fulfill these requisites,
but their performance was poor due to the impossibility of using GPUs to run them in
the last PyTorch release.
## Wasserstein generative adversarial network
The stability of traditional GANs is overcome by Wassertein generative adversarial networks
(WGAN), thus this algorithm is chosen over the traditional one for the study.
The WGAN algorithm is well explained in this [article](https://arxiv.org/abs/1701.07875) and its main difference with
the traditional GAN algorithm is that there is no longer a discriminator model but a critic
model. This model has to be trained till optimality so that it avoids modes collapse.
For this work the implementation of WGAN is made following the model in [here](https://github.com/wiseodd/generative-models/blob/master/GAN/wasserstein_gan/wgan_pytorch.py).
The architecture of the model is the same as the one depicted in 4.1, the only change is
that the "discriminator" module is in this case named "critic". The full configuration of
the generative model is in
# Results
Every combination of recurrent neural networks and convolutional neural networks,
as generator or critic, is tried. The best results are achieved by the utilization of CNN as
generator and critic, and are the ones presented in this section.
This chapter considers a visual comparison between the synthetic data (generated
after at least 4 hours of training) and real data. Additionally, it is compared the mean
root mean square (RMS) and mean peak to average ratio (PAR) of 100 generated time
series with 100 slices of the real time series.

Tables and analysis in the report.

# Further Steps
This work purposes a WGAN model to generate different mobile network parameters
as SNR, BSR, or decoding time. Although promising results are obtained for said
parameters, some limitations are addressed as the model struggles with emulating all
metrics simultaneously and low variance time series.

It is possible to say that the combination of CNNs as generator and critic performs
better than any combination with RNNs, as they lead to a less efficient (and therefore
slower) trainings.

Generally, parameters generated using datasets of Clone patterns outperform the
other cases in being similar to real data. This is a positive aspect given that Clone patterns
are the nearest to real use cases: they replicate actual traffic scenarios.
The SNR patterns have not shown to be very useful as the sudden changes of the
SNR values cannot be simulated with the purposed generative model. However, by using
them, more diverse scenarios have been created for the other parameters. Smoother
evolving SNR patterns might be more appropriate, but the repercussion of high frequency
requests of transmission gain modification should then be studied in detail.

It would be helpful to have a higher time resolution original dataset, in order to analyse
profoundly the time evolution of the metrics. Other further steps may include the
utilization of peak to average ratio metric in the training process, the implementation of
a WGAN with gradient penalty, or the utilization of automated hyperparameters tuning
algorithm.

# Acknowledgements
Machine Learning models based on: https://github.com/proceduralia/pytorch-GAN-timeseries/tree/master/models


Contact author: **Mario Rodríguez Ibáñez**  mario.ri39@gmail.com