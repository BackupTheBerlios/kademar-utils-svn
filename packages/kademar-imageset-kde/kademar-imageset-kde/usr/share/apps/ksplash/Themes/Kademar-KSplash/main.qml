//Caledonia KSplash theme in QML v1.3 was made by Malcer <malcer[at]gmx[dot]com> <sourceforge.net/projects/caledonia/> <malcer.deviantart.com>. 
//
//Some rights reserved. This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 License. | 2013
//https://creativecommons.org/licenses/by-sa/3.0/

// Kitline KSplash Theme v 0.1 is a fork of Caledonia KSplash Theme. Kitline was created by Ayoze Hernández Díaz <ayoze12@gmail.com>
// This work is under CC-BY-SA (Creative Commons Attribution-ShareAlike 3.0 License).                                       
// https://creativecommons.org/licenses/by-sa/3.0/                                                                          


import Qt 4.7

Item {
    id: main

    width: screenSize.width
    height: screenSize.height


    property int stage
    property int iconSize: (screenSize.width <= 1024) ? 32 : 64

    
    
    //  STEPS
    onStageChanged: {
        if (stage == 1) {
 
            background.opacity = 1
 
	    spin3.opacity = 1
 
        }
        if (stage == 2) {
 
	    spin.opacity = 0

        }
        if (stage == 3) {
 
            
	    spin.opacity = 1

        }
        if (stage == 4) {

	    spin2.opacity = 0
 
        }
        if (stage == 5) {

	    spin2.opacity = 1
 

 
        }
    }
    
    //  STEPS


// BACKGROUND

    Image {
        id: background
	source: "images/background.png"
	 anchors.fill: parent
 

        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }

        opacity: 0
 
    }


// BACKGROUND

    Image {
        id: logo
	source: "images/kademar-logo.png"
// 	 anchors.fill: background
x: (parent.width - width) /2
   y: ( (parent.height - height ) /3 ) *2

	opacity: 0
	
	Behavior on opacity { NumberAnimation { duration: 2000; easing { type: Easing.InOutQuad } } }
NumberAnimation on opacity {
        id: fadeAnimation
        from: 0
        to: 1
        duration: 2200
        }
 
    }


    
// ANIMATION


  Rectangle{
    id:frame
    width: 100
    height: 100
    color: "transparent"
    smooth: true
    
    x: (background.width - width) / 2
    y: (background.height - height) / 2
    
    opacity: 1
        Behavior on opacity { NumberAnimation { duration: 1000; easing { type: Easing.InOutQuad } } }

        NumberAnimation on opacity {
        id: frameAnimation
        from: 0
        to: 1
        duration: 800
        }
 
    Image {
        id: spin

        height: 48
        width: 48
        smooth: true

        x: (frame.width - width) / 6
        y: (frame.height - height) / 1.6

        source: "images/engine3.png"
	opacity: 0
	
	Behavior on opacity { NumberAnimation { duration: 2000; easing { type: Easing.InOutQuad } } }
        
        NumberAnimation {
            id: animateRotation
            target: spin
            properties: "rotation"
            from: 0
            to: 360
            duration: 2000

            loops: Animation.Infinite
            running: true
        }

    }
    
        Image {
        id: spin2

        height: 48
        width: 48
        smooth: true

        x: (frame.width - width) / 1.18
        y: (frame.height - height) / 10

        source: "images/engine2.png"
	opacity: 0
	
	Behavior on opacity { NumberAnimation { duration: 2000; easing { type: Easing.InOutQuad } } }

        NumberAnimation {
            id: animateRotation2
            target: spin2
            properties: "rotation"
            from: 360
            to: 0
            duration: 2000

            loops: Animation.Infinite
            running: true
        }

    }
    
            Image {
        id: spin3

        height: 28
        width: 28
        smooth: true

        x: (frame.width - width) / 1.54
        y: (frame.height - height) / 1.12

        source: "images/engine.png"
	opacity: 1
	
	Behavior on opacity { NumberAnimation { duration: 2000; easing { type: Easing.InOutQuad } } }
        
        NumberAnimation {
            id: animateRotation3
            target: spin3
            properties: "rotation"
            from: 360
            to: 0
            duration: 1500

            loops: Animation.Infinite
            running: true
        }

    }

  }
    
}

  
