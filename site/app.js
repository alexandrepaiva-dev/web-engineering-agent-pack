(() => {
  const data = window.WEAP_SITE || {};
  document.querySelectorAll("[data-version]").forEach(x => x.textContent = data.version ? `v${data.version}` : "");
  document.querySelectorAll("[data-skill-count]").forEach(x => x.textContent = data.skillCount ?? "33");
  document.querySelectorAll("[data-profile-count]").forEach(x => x.textContent = data.profiles?.length ?? "6");
  document.querySelectorAll("[data-repo-link]").forEach(x => { if (data.repositoryUrl) x.href = data.repositoryUrl; });
  const root = document.querySelector("[data-profiles]");
  if (!root) return;
  const render=(selector,items) => {
    const target=document.querySelector(selector);
    if (!target) return;
    (items || []).forEach(p => {
      const el=document.createElement("article");
      el.className="card";
      const chips=(p.skills || []).slice(0,6).map(s=>`<span class="chip">${s}</span>`).join("");
      el.innerHTML=`<h3>${p.name}</h3><p>${p.description || ""}</p><div class="chips">${chips}</div>`;
      target.appendChild(el);
    });
  };
  root.innerHTML="";
  render("[data-profiles]",data.profiles);
  render("[data-mcp-profiles]",data.mcpProfiles);
})();
