(function () {
  function postFeedback(payload) {
    return fetch("/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then(async function (res) {
      const body = await res.json().catch(function () {
        return {};
      });
      return { status: res.status, body: body };
    });
  }

  function init() {
    const root = document.querySelector(".property-detail-shell");
    if (!root) return;
    const propertyId = root.getAttribute("data-property-id");
    const searchId = root.getAttribute("data-search-id");
    const favoriteBtn = document.getElementById("favorite-btn");
    const requestBtn = document.getElementById("request-btn");
    const requestForm = document.getElementById("request-form");
    const resultNode = document.getElementById("property-action-result");

    function render(result) {
      if (resultNode) {
        resultNode.textContent = JSON.stringify(result, null, 2);
      }
    }

    async function send(action) {
      if (!propertyId || !searchId) return;
      render(await postFeedback({ request_id: searchId, property_id: propertyId, action: action }));
    }

    if (propertyId && searchId) {
      void send("detail_view");
    }

    favoriteBtn?.addEventListener("click", function () {
      void send("favorite");
    });

    requestBtn?.addEventListener("click", function () {
      if (requestForm) requestForm.hidden = false;
      void send("request_button_click");
    });

    requestForm?.addEventListener("submit", function (event) {
      event.preventDefault();
      void send("request_complete");
    });
  }

  init();
})();
