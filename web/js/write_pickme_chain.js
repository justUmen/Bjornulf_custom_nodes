import { app } from "../../../scripts/app.js";

// Helper function to clean up widget DOM elements
function cleanupWidgetDOM(widget) {
  if (widget && widget.inputEl) {
    if (widget.inputEl.parentElement) {
      widget.inputEl.parentElement.remove();
    } else {
      widget.inputEl.remove();
    }
  }
}

function getChainNodes(startNode) {
  const nodes = [];
  let currentNode = startNode;
  const visitedUpstream = new Set();

  // First traverse upstream to find the root node
  while (true) {
    if (visitedUpstream.has(currentNode.id)) {
      throw new Error(
        "Infinite loop detected! Nodes form a circular chain through 'pickme_chain' inputs"
      );
    }
    visitedUpstream.add(currentNode.id);

    const input = currentNode.inputs.find((i) => i.name === "pickme_chain");
    if (input?.link) {
      const link = app.graph.links[input.link];
      const prevNode = app.graph.getNodeById(link.origin_id);
      if (prevNode?.comfyClass === "Bjornulf_WriteTextPickMeChain") {
        currentNode = prevNode;
      } else {
        break;
      }
    } else {
      break;
    }
  }

  // Now traverse downstream from root
  const visitedDownstream = new Set();
  while (currentNode) {
    if (visitedDownstream.has(currentNode.id)) {
        app.ui.dialog.show("Infinite loop detected! Nodes form a circular chain through 'chain_text' outputs");
      throw new Error(
        "Infinite loop detected! Nodes form a circular chain through 'chain_text' outputs"
      );
    }
    visitedDownstream.add(currentNode.id);
    nodes.push(currentNode);

    const output = currentNode.outputs.find((o) => o.name === "chain_text");
    if (output?.links) {
      let nextNode = null;
      for (const linkId of output.links) {
        const link = app.graph.links[linkId];
        const targetNode = app.graph.getNodeById(link.target_id);
        if (targetNode?.comfyClass === "Bjornulf_WriteTextPickMeChain") {
          nextNode = targetNode;
          break;
        }
      }
      currentNode = nextNode;
    } else {
      break;
    }
  }

  return nodes;
}

function pickNode(node) {
    const chainNodes = getChainNodes(node);
    chainNodes.forEach(n => {
        const pickedWidget = n.widgets.find(w => w.name === "picked");
        if (pickedWidget) {
            const isPicked = n === node;
            pickedWidget.value = isPicked;
            n.color = isPicked ? "#006400" : "";
        }
    });
    app.graph.setDirtyCanvas(true, true);
}

function findAndPickNext(removedNode) {
    const chainNodes = getChainNodes(removedNode);
    const remaining = chainNodes.filter(n => n.id !== removedNode.id);
    if (remaining.length) pickNode(remaining[0]);
}

app.registerExtension({
  name: "Bjornulf.WriteTextPickMeChain",
  async nodeCreated(node) {
    if (node.comfyClass === "Bjornulf_WriteTextPickMeChain") {
      // Store original onRemoved if it exists
      const origOnRemoved = node.onRemoved;
      // Create widgets in specific order to maintain layout
      // const textWidget = node.widgets.find(w => w.name === "text");
      // if (textWidget) {
      //     textWidget.computeSize = function() {
      //         return [node.size[0] - 20, 150];
      //     };
      // }

      // Handle picked widget
      let pickedWidget = node.widgets.find((w) => w.name === "picked");
      if (!pickedWidget) {
        pickedWidget = node.addWidget("BOOLEAN", "picked", false, null);
      }
      pickedWidget.visible = false;

      // Add button after textarea
      const buttonWidget = node.addWidget("button", "PICK ME", null, () =>
        pickNode(node)
      );
      buttonWidget.computeSize = function () {
        return [node.size[0] - 20, 30];
      };

      // Set initial node size
      // node.size = [node.size[0], 200];
      // node.size = [200, 200];
      setTimeout(() => {
        // Update widget positions
        node.onResize(node.size);

        // Refresh all widgets
        node.widgets.forEach((w) => {
          if (w.onShow?.(true)) {
            w.onShow?.(false);
          }
        });

        app.graph.setDirtyCanvas(true, true);
      }, 10);

      // Enhanced cleanup on node removal
      node.onRemoved = function () {
        // Call original onRemoved if it exists
        if (origOnRemoved) {
          origOnRemoved.call(this);
        }

        // Handle chain updates
        if (this.widgets.find((w) => w.name === "picked")?.value) {
          findAndPickNext(this);
        }

        // Clean up all widgets
        for (const widget of this.widgets) {
          cleanupWidgetDOM(widget);
        }

        // Force DOM cleanup and canvas update
        if (this.domElement) {
          this.domElement.remove();
        }
        app.graph.setDirtyCanvas(true, true);
      };

      const updateColors = () => {
        const picked = node.widgets.find((w) => w.name === "picked")?.value;
        node.color = picked ? "#006400" : "";
      };

      const origSetNodeState = node.setNodeState;
      node.setNodeState = function (state) {
        origSetNodeState?.apply(this, arguments);
        if (state.picked !== undefined) {
          const widget = this.widgets.find((w) => w.name === "picked");
          if (widget) widget.value = state.picked;
        }
        updateColors();
      };

      const origGetNodeState = node.getNodeState;
      node.getNodeState = function () {
        const state = origGetNodeState?.apply(this, arguments) || {};
        state.picked =
          this.widgets.find((w) => w.name === "picked")?.value ?? false;
        return state;
      };

      // Force initial layout update
      app.graph.setDirtyCanvas(true, true);
    }
  },
});