/* 传奇发布网 · 站点脚本 */
(function () {
  "use strict";

  /* 移动端导航开关 */
  function bindNav() {
    var btn = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".nav");
    if (!btn || !nav) return;
    btn.addEventListener("click", function () {
      nav.classList.toggle("open");
      btn.textContent = nav.classList.contains("open") ? "收起导航" : "导航菜单";
    });
  }

  /* 顶部搜索框：跳转到搜索页 */
  function bindSearch() {
    var forms = document.querySelectorAll(".search form");
    Array.prototype.forEach.call(forms, function (f) {
      f.addEventListener("submit", function (e) {
        e.preventDefault();
        var input = f.querySelector("input");
        var kw = (input && input.value || "").trim();
        location.href = kw ? "search.html?q=" + encodeURIComponent(kw) : "search.html";
      });
    });
  }

  /* 搜索页渲染 */
  function renderSearch() {
    var box = document.getElementById("search-res");
    if (!box) return;
    var input = document.getElementById("kw");
    var data = window.SEARCH_DATA || [];
    var params = new URLSearchParams(location.search);
    var q = (params.get("q") || "").trim();
    if (input) input.value = q;

    function esc(s) {
      return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    if (!q) {
      box.innerHTML = '<p class="empty">输入关键词开始检索，例如「开区」「合击」「打金」「冰雪」。</p>';
      return;
    }
    var kw = q.toLowerCase();
    var res = data.filter(function (x) {
      var hay = (x.t + " " + x.d + " " + (x.k || "") + " " + (x.c || "")).toLowerCase();
      return hay.indexOf(kw) !== -1;
    });

    if (!res.length) {
      box.innerHTML =
        '<p class="empty">没有找到与「' + esc(q) + '」相关的内容。<br>可以试试更短的关键词，或直接查看 <a href="kaifu.html">今日开服表</a>。</p>';
      return;
    }
    var html = '<p class="list-count">共找到 ' + res.length + " 条相关内容</p>";
    res.slice(0, 40).forEach(function (x) {
      html +=
        '<div class="r"><h3><a href="' + esc(x.u) + '">' + esc(x.t) + "</a></h3>" +
        '<div class="m">' + esc(x.c) + " · " + esc(x.d) + "</div>" +
        "<p>" + esc(x.desc) + "</p></div>";
    });
    box.innerHTML = html;
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindNav();
    bindSearch();
    renderSearch();
  });
})();
