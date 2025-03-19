import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

// Helper function to construct image URLs for ComfyUI
function imageDataToUrl(data) {
  return api.apiURL(
    `/view?filename=${encodeURIComponent(data.filename)}&type=${
      data.type
    }&subfolder=${data.subfolder}` + app.getPreviewFormatParam()
  );
}

app.registerExtension({
  name: "Bjornulf.FourImageViewer",
  async nodeCreated(node) {
    // Ensure this applies only to the specific node type
    if (node.comfyClass !== "Bjornulf_FourImageViewer") return;

    // Constants for layout and sizing
    const marginTop = 90; // Space at the top for node UI elements
    const verticalOffset = -30; // Adjustment for canvas positioning
    const minSize = 256; // Minimum size of the node
    const maxSize = 2048; // Maximum size of the node
    const padding = 10; // Padding around the image area

    // Initialize node properties
    node.size = [512, 512 + marginTop];
    node.data = {
      images: new Array(4).fill(null), // Array to hold up to 4 images
      sliderX: null, // X position of the vertical slider
      sliderY: null, // Y position of the horizontal slider
    };

    // Enable resizing
    node.flags |= LiteGraph.RESIZABLE;

    // Handle resizing to maintain square aspect ratio
    node.onResize = function (size) {
      const minDimension = Math.max(
        minSize,
        Math.min(size[0], size[1] - marginTop)
      );
      const maxDimension = Math.min(maxSize, minDimension);
      size[0] = maxDimension;
      size[1] = maxDimension + marginTop;

      const fullImgWidth = size[0] - 3 * padding;
      const fullImgHeight = size[1] - padding - marginTop;

      // Update slider positions proportionally
      if (node.data.hasOwnProperty("sliderX")) {
        const oldWidth = node.size[0] - 3 * padding;
        const oldHeight = node.size[1] - padding - marginTop;
        const relativeX = (node.data.sliderX - padding) / oldWidth;
        const relativeY = (node.data.sliderY - marginTop) / oldHeight;
        node.data.sliderX = padding + fullImgWidth * relativeX;
        node.data.sliderY = marginTop + fullImgHeight * relativeY;
      } else {
        node.data.sliderX = padding + fullImgWidth / 2;
        node.data.sliderY = marginTop + fullImgHeight / 2;
      }

      node.size = size;
      return size;
    };

    // Handle mouse down to move sliders
    node.onMouseDown = function (e) {
      const rect = node.getBounding();
      const [clickX, clickY] = [
        e.canvasX - rect[0],
        e.canvasY - rect[1] + verticalOffset,
      ];

      const xStart = padding;
      const xEnd = xStart + (node.size[0] - 3 * padding);
      const yStart = marginTop;
      const yEnd = yStart + (node.size[1] - padding - marginTop);

      if (
        clickX >= xStart &&
        clickX <= xEnd &&
        clickY >= yStart &&
        clickY <= yEnd
      ) {
        const hasImage2 = node.data.images[1] !== null;
        const hasImage3 = node.data.images[2] !== null;
        const hasImage4 = node.data.images[3] !== null;

        // Lock sliderY to bottom if only two images are present
        if (hasImage2 && !hasImage3 && !hasImage4) {
          node.data.sliderY = yEnd;
        }

        node.data.sliderX = Math.max(xStart, Math.min(clickX, xEnd));
        node.data.sliderY =
          hasImage3 || hasImage4
            ? Math.max(yStart, Math.min(clickY, yEnd))
            : yEnd;

        app.graph.setDirtyCanvas(true, true);
        return true;
      }
      return false;
    };

    // Load images when the node is executed
    node.onExecuted = async function (message) {
      node.data.images = new Array(4).fill(null);
      for (let i = 1; i <= 4; i++) {
        const images = message[`images_${i}`] || [];
        if (images.length) {
          const imgData = images[0];
          const img = new Image();
          img.src = imageDataToUrl(imgData);
          await new Promise((resolve) => (img.onload = img.onerror = resolve));
          node.data.images[i - 1] = img;
        }
      }
      app.graph.setDirtyCanvas(true, true);
    };

    // Render images and sliders
    node.onDrawForeground = function (ctx) {
      const xStart = padding;
      const xEnd = xStart + (node.size[0] - 3 * padding);
      const yStart = marginTop;
      const yEnd = yStart + (node.size[1] - padding - marginTop);
      const fullImgWidth = node.size[0] - 3 * padding;
      const fullImgHeight = node.size[1] - padding - marginTop;

      // Calculate fitted rectangle for image display
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

      // Draw a cropped image within specified bounds
      function drawCroppedImage(img, dx, dy, dWidth, dHeight) {
        if (!img) return;
        let targetRatio = dWidth / dHeight;
        if (
          node.data.images[0] &&
          node.data.images[0].naturalWidth &&
          node.data.images[0].naturalHeight
        ) {
          targetRatio =
            node.data.images[0].naturalWidth /
            node.data.images[0].naturalHeight;
        }

        const [ndx, ndy, ndWidth, ndHeight] = getFittedDestRect(
          dx,
          dy,
          dWidth,
          dHeight,
          targetRatio
        );

        const imgRatio = img.naturalWidth / img.naturalHeight;
        let sx = 0,
          sy = 0,
          sWidth = img.naturalWidth,
          sHeight = img.naturalHeight;
        if (imgRatio > targetRatio) {
          sWidth = img.naturalHeight * targetRatio;
          sx = (img.naturalWidth - sWidth) / 2;
        } else if (imgRatio < targetRatio) {
          sHeight = img.naturalWidth / targetRatio;
          sy = (img.naturalHeight - sHeight) / 2;
        }
        ctx.drawImage(
          img,
          sx,
          sy,
          sWidth,
          sHeight,
          ndx,
          ndy,
          ndWidth,
          ndHeight
        );
      }

      const connectedImages = node.data.images
        .slice(1)
        .filter((img) => img !== null).length;

      if (connectedImages === 0) {
        // Single image display
        if (node.data.images[0]) {
          drawCroppedImage(
            node.data.images[0],
            xStart,
            yStart,
            fullImgWidth,
            fullImgHeight
          );
        }
      } else if (connectedImages === 1 && node.data.images[1]) {
        // Two images with vertical split
        const splitX = node.data.sliderX;
        ctx.save();
        ctx.beginPath();
        ctx.rect(xStart, yStart, splitX - xStart, fullImgHeight);
        ctx.clip();
        drawCroppedImage(
          node.data.images[0],
          xStart,
          yStart,
          fullImgWidth,
          fullImgHeight
        );
        ctx.restore();

        ctx.save();
        ctx.beginPath();
        ctx.rect(splitX, yStart, xEnd - splitX, fullImgHeight);
        ctx.clip();
        drawCroppedImage(
          node.data.images[1],
          xStart,
          yStart,
          fullImgWidth,
          fullImgHeight
        );
        ctx.restore();
      } else {
        // Three or four images with quadrants
        const drawQuadrant = (imgIndex, clipX, clipY, clipW, clipH) => {
          if (!node.data.images[imgIndex]) return;
          ctx.save();
          ctx.beginPath();
          ctx.rect(clipX, clipY, clipW, clipH);
          ctx.clip();
          drawCroppedImage(
            node.data.images[imgIndex],
            xStart,
            yStart,
            fullImgWidth,
            fullImgHeight
          );
          ctx.restore();
        };

        drawQuadrant(
          0,
          xStart,
          yStart,
          node.data.sliderX - xStart,
          node.data.sliderY - yStart
        );
        drawQuadrant(
          1,
          node.data.sliderX,
          yStart,
          xEnd - node.data.sliderX,
          node.data.sliderY - yStart
        );

        if (node.data.images[3] === null) {
          drawQuadrant(
            2,
            xStart,
            node.data.sliderY,
            xEnd - xStart,
            yEnd - node.data.sliderY
          );
        } else {
          drawQuadrant(
            2,
            xStart,
            node.data.sliderY,
            node.data.sliderX - xStart,
            yEnd - node.data.sliderY
          );
          drawQuadrant(
            3,
            node.data.sliderX,
            node.data.sliderY,
            xEnd - node.data.sliderX,
            yEnd - node.data.sliderY
          );
        }
      }

      // Draw sliders
      ctx.strokeStyle = "#FFF";
      ctx.lineWidth = 1;
      if (connectedImages > 0) {
        ctx.beginPath();
        if (node.data.images[3] === null && node.data.images[2] !== null) {
          ctx.moveTo(node.data.sliderX, yStart);
          ctx.lineTo(node.data.sliderX, node.data.sliderY);
        } else {
          ctx.moveTo(node.data.sliderX, yStart);
          ctx.lineTo(node.data.sliderX, yEnd);
        }
        if (connectedImages >= 2) {
          ctx.moveTo(xStart, node.data.sliderY);
          ctx.lineTo(xEnd, node.data.sliderY);
        }
        ctx.stroke();
      }
    };
  },
});
