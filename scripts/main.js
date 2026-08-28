//Imports
import * as THREE from 'three';
import { Reflector } from 'three/addons/objects/Reflector.js';

//Boilerplate
const scene = new THREE.Scene();
const container = document.getElementById("scene-container");

scene.background = new THREE.Color(0x00799D);
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setAnimationLoop( animate );

renderer.setSize(
    container.clientWidth,
    container.clientHeight
);

container.appendChild( renderer.domElement );

//lighting

const intensity = 1;
const color = 0xFFFFFF;
const light1 = new THREE.DirectionalLight(color, intensity);
light1.position.set(10, 10, 0);
light1.target.position.set(2, 0, 0);
scene.add(light1);
scene.add(light1.target);



//Plane / tank

const planeSize = 40;
 
const loader = new THREE.TextureLoader();
const texture = loader.load('../images/sand.jpg');
texture.wrapS = THREE.RepeatWrapping;
texture.wrapT = THREE.RepeatWrapping;
texture.magFilter = THREE.NearestFilter;
texture.colorSpace = THREE.SRGBColorSpace;
const repeats = planeSize / 2;
texture.repeat.set(repeats, repeats);

const planeGeo = new THREE.PlaneGeometry(planeSize, planeSize/4);
const planeMat = new THREE.MeshPhongMaterial({
  map: texture,
  side: THREE.DoubleSide,
});
const mesh = new THREE.Mesh(planeGeo, planeMat);
mesh.rotation.x = Math.PI * -.5;
scene.add(mesh);


const backGlassGeo = new THREE.PlaneGeometry(planeSize, planeSize);
const backGlassMat = new THREE.MeshPhongMaterial( { color: 0xffffff } );
const backGlassMesh = new THREE.Mesh(backGlassGeo, backGlassMat);
backGlassMesh.material.transparent = true;
backGlassMesh.material.opacity = 0.1;
backGlassMesh.position.z = -2;
scene.add(backGlassMesh);

/*
const geometry1 = new THREE.BoxGeometry( 40, 11, 5 );
const material1 = new THREE.MeshPhongMaterial( { color: 0xffffff } );
const cube1 = new THREE.Mesh( geometry1, material1 );
cube1.material.transparent = true;
cube1.material.opacity = 0.1;
cube1.material.side = THREE.DoubleSide;
scene.add( cube1 );
*/

//end tank


//spinning cube

const geometry = new THREE.BoxGeometry( 1, 1, 1 );
const material = new THREE.MeshPhongMaterial( { color: 0xc9f040 } );
const cube = new THREE.Mesh( geometry, material );
//scene.add( cube );

//end spinning cube

//fish??

const fishGeo = new THREE.OctahedronGeometry();
const fishMat = new THREE.MeshPhongMaterial( { color: 0xc9f040 } );
const fish = new THREE.Mesh( fishGeo, fishMat );

const fishPos = fish.geometry.getAttribute("position");
console.log(fishPos.array);
fishPos.array[0] = fishPos.array[0]+0.2;


scene.add( fish );

//end fish??




camera.position.z = 5;
camera.position.set(0, 5, 5);
camera.lookAt(0, 3, 0);




//garden eel

const points = [
  new THREE.Vector3(5, -3, 0),
  new THREE.Vector3(6, 1, 0),
  new THREE.Vector3(6.2, 2, 0),
  new THREE.Vector3(6.2, 3, 0),
  new THREE.Vector3(6, 4, 0),
  new THREE.Vector3(5, 4.8, 0),
  //head
  new THREE.Vector3(4, 5, 0),
  new THREE.Vector3(3.8, 5, 0),
  new THREE.Vector3(3, 4.8, 0), //nose and eye anchor
  new THREE.Vector3(3.5, 4.8, 0),
  new THREE.Vector3(3.8, 5, 0),
];

const originalPoints = structuredClone(points);
const curve = new THREE.CatmullRomCurve3(points);
const tuber = new THREE.TubeGeometry(
  curve,
  100, // tubular segments
  0.2, // radius
  16,  // radial segments
  false // closed loop?
);
const tubematerial = new THREE.MeshStandardMaterial({
  color: 0x00ffcc
});
const tube = new THREE.Mesh(tuber, tubematerial);


const noseGeometry = new THREE.SphereGeometry( .2, 32, 16 );
const nose = new THREE.Mesh( noseGeometry, tubematerial );

console.log(points.at(-3));
nose.position.x=points.at(-3).x;
nose.position.y=points.at(-3).y;
nose.position.z=points.at(-3).z;


const outerGeometry = new THREE.SphereGeometry( .15, 32, 16 );
const outerMaterial = new THREE.MeshBasicMaterial( { color: 0xc9f040 } );
const eyeOuter = new THREE.Mesh( outerGeometry, outerMaterial );
eyeOuter.position.x=points.at(-3).x+0.1;
eyeOuter.position.y=points.at(-3).y+0.05;
eyeOuter.position.z=points.at(-3).z+0.12;

const innerGeometry = new THREE.SphereGeometry( .1, 32, 16 );
const innerMaterial = new THREE.MeshStandardMaterial( { color: 0x000000 } );
const eyeInner = new THREE.Mesh( innerGeometry, innerMaterial );
eyeInner.position.x=eyeOuter.position.x;
eyeInner.position.y=eyeOuter.position.y;
eyeInner.position.z=eyeOuter.position.z+0.09;

const pos = tuber.attributes.position;

scene.add(tube);
scene.add( nose );
scene.add( eyeOuter );
scene.add( eyeInner );

//end garden eel


//reflection
/* 
Instead of doing this, I should have an if (mirror) {} block that basically 
says duplicate all the objects in the tank and make another one over some axis
but flipped, and transparent. See this for example
https://github.com/mrdoob/three.js/blob/master/examples/webgl_geometry_text.html#L325
It's possible I could also do a custom shader as shown here
https://jsfiddle.net/kyw9s2vL/2/
but I have a following that will be computationally heavier. Still, could be
a good exercise in shader building.
*/
const refgeometry = new THREE.PlaneGeometry( 100, 100 );
const refreflector = new Reflector( refgeometry, {
	clipBias: 0.003,
	textureWidth: window.innerWidth * window.devicePixelRatio,
	textureHeight: window.innerHeight * window.devicePixelRatio,
	color: 0xc1cbcb
} );
refreflector.position.z = -2.2;
refreflector.material.transparent = true;
refreflector.material.opacity = 0.1;


scene.add( refreflector );

//end reflection


function animate( time ) {
    light1.position.x = Math.sin(time / 100)/2;
    light1.intensity = 1+Math.sin(time / 500)/2;
    //octahedron.rotation.x = time / 1000;
    //octahedron.rotation.y = time / 1000;
    fish.position.y = 2+Math.sin(time / 1000)/2;

    camera.rotation.y = Math.sin(time / 500)/200;
    camera.position.y = camera.position.y+Math.sin(time / 500)/100;
    camera.position.x = camera.position.x+Math.cos(time / 5000)/100;


    /*
    for(let i=0; i<pos.count; i++){
        if(i%30===0){
            const x = pos.getX(i);
            const y = pos.getY(i);
            const z = pos.getZ(i);
            pos.setXYZ(i, x+Math.sin(time/100),y,z);
        }
        //pos = tuber.attributes.position;
    }*/

    //move head
    for(let i=points.length-1; i>=points.length-5; i--){
        points[i].x = originalPoints[i].x+(Math.sin(time/200)/3);
        points[i].y = originalPoints[i].y+(Math.cos(time/250)/10);
    }
    //move body
    for(let i=points.length-6; i>1; i--){
        points[i].x = originalPoints[i].x+(Math.sin(time/200+i)/5);
    }

    nose.position.x=points.at(-3).x;
    nose.position.y=points.at(-3).y;
    nose.position.z=points.at(-3).z;
    eyeOuter.position.x=points.at(-3).x+0.1;
    eyeOuter.position.y=points.at(-3).y+0.05;
    eyeOuter.position.z=points.at(-3).z+0.12;
    eyeInner.position.x=eyeOuter.position.x;
    eyeInner.position.y=eyeOuter.position.y;
    eyeInner.position.z=eyeOuter.position.z+0.09;



    curve.points = points;
    tube.geometry.dispose();
    tube.geometry = new THREE.TubeGeometry(
        curve,
        100, // tubular segments
        0.2, // radius
        16,  // radial segments
        false // closed loop?
    );
    //console.log(points);

    renderer.render( scene, camera );

}