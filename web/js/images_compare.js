import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

function imageDataToUrl(data) {
  return api.apiURL(
    `/view?filename=${encodeURIComponent(data.filename)}&type=${data.type}&subfolder=${data.subfolder}${app.getPreviewFormatParam()}`
  );
}

app.registerExtension({
  name: "Bjornulf.FourImageViewer",
  async nodeCreated(node) {
    if (node.comfyClass !== "Bjornulf_FourImageViewer") return;

    const marginTop = 90;
    const verticalOffset = -30;
    const minSize = 256; // Minimum size for the node
    const maxSize = 2048; // Maximum size for the node
    node.size = [512, 512 + marginTop];
    node.images = new Array(4).fill(null);
    const padding = 10;

    // Add resize handles
    node.flags |= LiteGraph.RESIZABLE;

    node.onResize = function(size) {
      // Ensure square aspect ratio (excluding marginTop)
      const minDimension = Math.max(minSize, Math.min(size[0], size[1] - marginTop));
      const maxDimension = Math.min(maxSize, minDimension);
      size[0] = maxDimension;
      size[1] = maxDimension + marginTop;
      
      // Update slider positions proportionally
      const fullImgWidth = size[0] - 3 * padding;
      const fullImgHeight = size[1] - padding - marginTop;
      
      // Only update sliders if they exist (node has been initialized)
      if (node.hasOwnProperty('sliderX')) {
        const oldWidth = node.size[0] - 3 * padding;
        const oldHeight = node.size[1] - padding - marginTop;
        
        // Calculate relative positions (0 to 1)
        const relativeX = (node.sliderX - padding) / oldWidth;
        const relativeY = (node.sliderY - marginTop) / oldHeight;
        
        // Update slider positions
        node.sliderX = padding + (fullImgWidth * relativeX);
        node.sliderY = marginTop + (fullImgHeight * relativeY);
      } else {
        // Initial slider positions
        node.sliderX = padding + fullImgWidth / 2;
        node.sliderY = marginTop + fullImgHeight / 2;
      }
      
      node.size = size;
      return size;
    };
    
    // Full area where images get drawn
    const fullImgWidth = node.size[0] - 3 * padding;
    const fullImgHeight = node.size[1] - padding - marginTop;
    node.sliderX = padding + fullImgWidth / 2;
    node.sliderY = marginTop + fullImgHeight / 2;

    node.onMouseDown = function(e) {
      const rect = node.getBounding();
      const [clickX, clickY] = [
        e.canvasX - rect[0],
        e.canvasY - rect[1] + verticalOffset
      ];
      
      const imgWidth = rect[2] - 3 * padding;
      const imgHeight = rect[3] - padding - marginTop;
      const xStart = padding;
      const xEnd = xStart + imgWidth;
      const yStart = marginTop;
      const yEnd = yStart + imgHeight;

      if (clickX >= xStart && clickX <= xEnd && clickY >= yStart && clickY <= yEnd) {
        const hasImage2 = node.images[1] !== null;
        const hasImage3 = node.images[2] !== null;
        const hasImage4 = node.images[3] !== null;
        if (hasImage2 && !hasImage3 && !hasImage4) {
          node.sliderY = yEnd;
        }
        node.sliderX = Math.max(xStart, Math.min(clickX, xEnd));
        node.sliderY = hasImage3 || hasImage4 
          ? Math.max(yStart, Math.min(clickY, yEnd))
          : yEnd;
        app.graph.setDirtyCanvas(true, true);
        return true;
      }
      return false;
    };

    node.onExecuted = async function(message) {
      node.images = new Array(4).fill(null);
      for (let i = 1; i <= 4; i++) {
        const images = message[`images_${i}`] || [];
        if (images.length) {
          const imgData = images[0];
          const img = new Image();
          img.src = imageDataToUrl(imgData);
          await new Promise(resolve => (img.onload = img.onerror = resolve));
          node.images[i - 1] = img;
        }
      }
      app.graph.setDirtyCanvas(true, true);
    };

    node.onDrawForeground = function(ctx) {
      const padding = 10;
      const xStart = padding;
      const xEnd = xStart + (node.size[0] - 3 * padding);
      const yStart = marginTop;
      const yEnd = yStart + (node.size[1] - padding - marginTop);
      const fullImgWidth = node.size[0] - 3 * padding;
      const fullImgHeight = node.size[1] - padding - marginTop;
  
      function getFittedDestRect(dx, dy, dWidth, dHeight, targetRatio) {
        let newWidth = dWidth;
        let newHeight = dWidth / targetRatio;
        if (newHeight > dHeight) {
          newHeight = dHeight;
          newWidth = dHeight * targetRatio;
        }
        const offsetX = dx + (dWidth - newWidth) / 2;
        const offsetY = dy + (dHeight - newHeight) / 2;
        return [offsetX, offsetY, newWidth, newHeight];
      }
  
      function drawCroppedImage(img, dx, dy, dWidth, dHeight) {
        if (!img) return;
        let targetRatio = dWidth / dHeight;
        if (node.images[0] && node.images[0].naturalWidth && node.images[0].naturalHeight) {
          targetRatio = node.images[0].naturalWidth / node.images[0].naturalHeight;
        }
  
        const [ndx, ndy, ndWidth, ndHeight] = getFittedDestRect(dx, dy, dWidth, dHeight, targetRatio);
  
        const imgRatio = img.naturalWidth / img.naturalHeight;
        let sx = 0, sy = 0, sWidth = img.naturalWidth, sHeight = img.naturalHeight;
        if (imgRatio > targetRatio) {
          sWidth = img.naturalHeight * targetRatio;
          sx = (img.naturalWidth - sWidth) / 2;
        } else if (imgRatio < targetRatio) {
          sHeight = img.naturalWidth / targetRatio;
          sy = (img.naturalHeight - sHeight) / 2;
        }
        ctx.drawImage(img, sx, sy, sWidth, sHeight, ndx, ndy, ndWidth, ndHeight);
      }
  
      const connectedImages = node.images.slice(1).filter(img => img !== null).length;
  
      if (connectedImages === 0) {
        if (node.images[0]) {
          drawCroppedImage(node.images[0], xStart, yStart, fullImgWidth, fullImgHeight);
        }
      } else if (connectedImages === 1 && node.images[1]) {
        const splitX = node.sliderX;
        ctx.save();
        ctx.beginPath();
        ctx.rect(xStart, yStart, splitX - xStart, fullImgHeight);
        ctx.clip();
        drawCroppedImage(node.images[0], xStart, yStart, fullImgWidth, fullImgHeight);
        ctx.restore();
  
        ctx.save();
        ctx.beginPath();
        ctx.rect(splitX, yStart, xEnd - splitX, fullImgHeight);
        ctx.clip();
        drawCroppedImage(node.images[1], xStart, yStart, fullImgWidth, fullImgHeight);
        ctx.restore();
      } else {
        const drawQuadrant = (imgIndex, clipX, clipY, clipW, clipH) => {
          if (!node.images[imgIndex]) return;
          ctx.save();
          ctx.beginPath();
          ctx.rect(clipX, clipY, clipW, clipH);
          ctx.clip();
          drawCroppedImage(node.images[imgIndex], xStart, yStart, fullImgWidth, fullImgHeight);
          ctx.restore();
        };
  
        drawQuadrant(0, xStart, yStart, node.sliderX - xStart, node.sliderY - yStart);
        drawQuadrant(1, node.sliderX, yStart, xEnd - node.sliderX, node.sliderY - yStart);
  
        if (node.images[3] === null) {
          drawQuadrant(2, xStart, node.sliderY, xEnd - xStart, yEnd - node.sliderY);
        } else {
          drawQuadrant(2, xStart, node.sliderY, node.sliderX - xStart, yEnd - node.sliderY);
          drawQuadrant(3, node.sliderX, node.sliderY, xEnd - node.sliderX, yEnd - node.sliderY);
        }
      }
  
      ctx.strokeStyle = "#FFF";
      ctx.lineWidth = 1;
      if (connectedImages > 0) {
        ctx.beginPath();
        ctx.moveTo(node.sliderX, yStart);
        ctx.lineTo(node.sliderX, yEnd);
        if (connectedImages >= 2) {
          ctx.moveTo(xStart, node.sliderY);
          ctx.lineTo(xEnd, node.sliderY);
        }
        ctx.stroke();
      }
    };
  },
});