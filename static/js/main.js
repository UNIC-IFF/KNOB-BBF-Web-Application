"use strict";

const feather = require("feather-icons");


import { initPageLoader } from './libs/components/pageloader/pageloader';
import './libs/components'

const showPageloader = initPageLoader();

document.onreadystatechange = function () {
  if (document.readyState == "complete") {
    //Switch demo images
    const changeImages = switchDemoImages(env);

    //Switch backgrounds
    const changeBackgrounds = insertBgImages();

    //Feather Icons
    const featherIcons = feather.replace();
  }
};
