// web/desktop/scene.js
/**
 * GAIA Three.js Scene - Living Desktop Environment
 * The World Tree, Holographic Panels, and Avatar Orb
 * Where technology and nature are siblings, not opposites.
 * 
 * Factor 11 (Order): Deterministic rendering pipeline
 * Factor 10 (Chaos): Organic, breathing animations
 * Factor 12 (Balance): Sacred geometry meets cybernetic beauty
 */

import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

export class GAIADesktopScene {
  constructor(containerElement) {
    this.container = containerElement;
    this.scene = new THREE.Scene();
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    
    // GAIA entities
    this.worldTree = null;
    this.avatarOrb = null;
    this.holoPanels = {};
    
    // State
    this.currentZScore = 5.5;
    this.crisisMode = false;
    
    this.init();
  }
  
  init() {
    // Camera setup - perspective view
    this.camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    this.camera.position.set(0, 5, 10);
    
    // Renderer - WebGL with antialiasing
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.container.appendChild(this.renderer.domElement);
    
    // Background - deep space gradient
    this.scene.background = new THREE.Color(0x0a0a0a);
    this.scene.fog = new THREE.Fog(0x0a0a0a, 50, 100);
    
    // Lighting - natural, warm, sacred
    this.setupLighting();
    
    // Entities
    this.createAvatarOrb();
    this.createHolographicPanels();
    this.createProceduralTree();
    
    // Controls - orbit around the scene
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.minDistance = 5;
    this.controls.maxDistance = 50;
    
    // Window resize handler
    window.addEventListener('resize', () => this.onWindowResize());
    
    // Start animation loop
    this.animate();
  }
  
  setupLighting() {
    // Ambient light - soft, pervasive
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    this.scene.add(ambientLight);
    
    // Sunlight - directional, warm
    const sunlight = new THREE.DirectionalLight(0xffffee, 0.8);
    sunlight.position.set(10, 20, 10);
    sunlight.castShadow = true;
    sunlight.shadow.camera.left = -20;
    sunlight.shadow.camera.right = 20;
    sunlight.shadow.camera.top = 20;
    sunlight.shadow.camera.bottom = -20;
    this.scene.add(sunlight);
    
    // Moonlight - soft blue accent
    const moonlight = new THREE.DirectionalLight(0x8888ff, 0.2);
    moonlight.position.set(-10, 10, -10);
    this.scene.add(moonlight);
  }
  
  createAvatarOrb() {
    /**
     * Avatar as glowing orb - will evolve to full form in Phase 3
     * Opposite-gender complement, moral compass, companion
     */
    const geometry = new THREE.SphereGeometry(0.5, 32, 32);
    const material = new THREE.MeshStandardMaterial({
      color: 0x00ffff,
      emissive: 0x00ffff,
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.8,
      roughness: 0.2,
      metalness: 0.8
    });
    
    this.avatarOrb = new THREE.Mesh(geometry, material);
    this.avatarOrb.position.set(3, 3, 0);
    this.avatarOrb.castShadow = true;
    this.scene.add(this.avatarOrb);
    
    // Add glow effect
    const glowGeometry = new THREE.SphereGeometry(0.6, 32, 32);
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: 0x00ffff,
      transparent: true,
      opacity: 0.3,
      side: THREE.BackSide
    });
    const glow = new THREE.Mesh(glowGeometry, glowMaterial);
    this.avatarOrb.add(glow);
  }
  
  createHolographicPanels() {
    // Z Score Panel - left side
    this.holoPanels.zscore = this.createPanel({
      position: { x: -6, y: 3, z: 0 },
      title: 'Z Score',
      color: 0x00ff88,
      size: { width: 3, height: 2 }
    });
    
    // Crystal Matrix Panel - right side
    this.holoPanels.matrix = this.createPanel({
      position: { x: 6, y: 3, z: 0 },
      title: 'Crystal Matrix',
      color: 0xff0088,
      size: { width: 3, height: 2 }
    });
    
    // Equilibrium Panel - top
    this.holoPanels.equilibrium = this.createPanel({
      position: { x: 0, y: 6, z: 0 },
      title: 'Equilibrium',
      color: 0xffaa00,
      size: { width: 4, height: 1.5 }
    });
  }
  
  createPanel(config) {
    const group = new THREE.Group();
    
    // Panel background - holographic glass
    const geometry = new THREE.PlaneGeometry(config.size.width, config.size.height);
    const material = new THREE.MeshStandardMaterial({
      color: config.color,
      transparent: true,
      opacity: 0.2,
      emissive: config.color,
      emissiveIntensity: 0.3,
      side: THREE.DoubleSide,
      roughness: 0.1,
      metalness: 0.9
    });
    
    const panel = new THREE.Mesh(geometry, material);
    group.add(panel);
    
    // Border glow
    const borderGeometry = new THREE.EdgesGeometry(geometry);
    const borderMaterial = new THREE.LineBasicMaterial({
      color: config.color,
      linewidth: 2
    });
    const border = new THREE.LineSegments(borderGeometry, borderMaterial);
    group.add(border);
    
    group.position.set(config.position.x, config.position.y, config.position.z);
    group.userData = { title: config.title, color: config.color };
    
    this.scene.add(group);
    return group;
  }
  
  createProceduralTree() {
    const treeGroup = new THREE.Group();
    
    // Trunk
    const trunkGeometry = new THREE.CylinderGeometry(0.3, 0.5, 5, 12);
    const trunkMaterial = new THREE.MeshStandardMaterial({
      color: 0x8b4513,
      roughness: 0.8,
      emissive: 0x00ff00,
      emissiveIntensity: 0.1
    });
    const trunk = new THREE.Mesh(trunkGeometry, trunkMaterial);
    trunk.position.y = 2.5;
    trunk.castShadow = true;
    treeGroup.add(trunk);
    
    // Canopy - glowing Viriditas energy
    const canopyGeometry = new THREE.SphereGeometry(2, 16, 16);
    const canopyMaterial = new THREE.MeshStandardMaterial({
      color: 0x00ff00,
      emissive: 0x00ff00,
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.6,
      roughness: 0.3
    });
    const canopy = new THREE.Mesh(canopyGeometry, canopyMaterial);
    canopy.position.y = 6;
    treeGroup.add(canopy);
    
    this.worldTree = treeGroup;
    this.scene.add(treeGroup);
  }
  
  updateZScore(zScore) {
    this.currentZScore = zScore;
    const color = this.zScoreToColor(zScore);
    
    if (this.worldTree) {
      this.worldTree.traverse((child) => {
        if (child.isMesh && child.material.emissive) {
          child.material.emissive = new THREE.Color(color);
          child.material.emissiveIntensity = 0.3 + (zScore / 12) * 0.5;
        }
      });
    }
    
    // Update Z Score panel
    if (this.holoPanels.zscore) {
      const panel = this.holoPanels.zscore.children[0];
      panel.material.emissive = new THREE.Color(color);
      panel.material.emissiveIntensity = 0.5;
    }
  }
  
  zScoreToColor(z) {
    if (z < 2) return 0xff0000; // Red - crisis
    if (z < 4) return 0xff6600; // Orange
    if (z < 6) return 0xffaa00; // Yellow
    if (z < 8) return 0x00ff00; // Green - healthy
    if (z < 10) return 0x00aaff; // Cyan
    return 0x8800ff; // Purple - transcendent
  }
  
  triggerCrisisMode(crisisData) {
    this.crisisMode = true;
    
    // Pulsing red light
    const crisisLight = new THREE.PointLight(0xff0000, 2, 50);
    crisisLight.position.set(0, 5, 0);
    crisisLight.name = 'crisisLight';
    this.scene.add(crisisLight);
    
    // Avatar intensifies
    if (this.avatarOrb) {
      this.avatarOrb.material.emissiveIntensity = 1.0;
      this.avatarOrb.scale.set(1.5, 1.5, 1.5);
    }
    
    console.warn('[CRISIS MODE ACTIVATED]', crisisData);
  }
  
  exitCrisisMode() {
    this.crisisMode = false;
    const crisisLight = this.scene.getObjectByName('crisisLight');
    if (crisisLight) this.scene.remove(crisisLight);
    
    if (this.avatarOrb) {
      this.avatarOrb.material.emissiveIntensity = 0.5;
      this.avatarOrb.scale.set(1, 1, 1);
    }
  }
  
  animate() {
    requestAnimationFrame(() => this.animate());
    
    // Avatar breathing
    if (this.avatarOrb) {
      const time = Date.now() * 0.001;
      this.avatarOrb.position.y = 3 + Math.sin(time) * 0.2;
      this.avatarOrb.rotation.y += 0.005;
    }
    
    // Holographic panels float
    Object.values(this.holoPanels).forEach((panel, i) => {
      const time = Date.now() * 0.001 + i;
      panel.position.y += Math.sin(time * 0.5) * 0.002;
    });
    
    // Crisis pulsing
    if (this.crisisMode) {
      const crisisLight = this.scene.getObjectByName('crisisLight');
      if (crisisLight) {
        crisisLight.intensity = 2 + Math.sin(Date.now() * 0.01) * 1;
      }
    }
    
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
  
  onWindowResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }
  
  dispose() {
    this.renderer.dispose();
    this.controls.dispose();
    window.removeEventListener('resize', () => this.onWindowResize());
  }
}
