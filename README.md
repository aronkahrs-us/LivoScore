<h1 align="center">LivoScore</h1>

<p align="center">
  <a href="">
    <img alt="LivoScore" title="LivoScore" src="assets/LivoScore.png" width="150">
  </a>
</p>

<p align="center">
  Your right hand for volleyball streams. All graphics and stats automated.
</p>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Configuration](#configuration)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

LivoScore provides graphics automation for volleyball matches. If you are streaming a match and its scoreboard is live on [DataProject's WCM](https://dataproject.com/Products/EU/en/Volleyball/WCM), you can automate the scoreboard and stats graphics. It is compatible with vMix and OBS.

**Disclaimer:** This version may not work with OBS. Development initially targeted OBS but transitioned to vMix, so OBS support may be limited or broken.

<p align="center">
  <img src="./assets/Livoscore1.png" width="250">
</p>

<p align="center">
  <img src="./assets/Livoscore2.png" width="350">
</p>

## Features

Here are some of the features LivoScore offers:

- Automated Scoreboard graphics
- Automated Match Statistics graphics
- Automated Championship Statistics graphics
- Automated Team Statistics graphics
- Automated Player Statistics graphics
- Automated Time Out graphics
- Automated Set and Match point graphics
- Automated Referee graphics
- Automated Player formation graphics

<p align="center">
  <img src="./assets/Livoscore3.png" width="700">
</p>

<p align="center">
  <img src="./assets/Livoscore4.png" width="700">
</p>

<p align="center">
  <img src="./assets/Livoscore5.png" width="700">
</p>

<p align="center">
  <img src="./assets/Livoscore6.png" width="700">
</p>

## Configuration

First, configure the connection to your streaming software, either OBS or vMix (note that OBS compatibility may be limited). Set the IP address (use "localhost" if LivoScore and your streaming software are on the same PC), along with the port and password for your streaming software's websocket.

<p align="center">
  <img src="./assets/Livoscore-config1.png" width="700">
</p>

Next, choose the league for the match you are streaming. Optionally, you can filter by team name if you only stream matches for one team.

<p align="center">
  <img src="./assets/Livoscore-config2.png" width="700">
</p>

Finally, configure the elements to display data, scores, and stats. This step requires knowing the names of the elements that correspond to the data you want to display.

<p align="center">
  <img src="./assets/Livoscore-config3.png" width="700">
</p>
