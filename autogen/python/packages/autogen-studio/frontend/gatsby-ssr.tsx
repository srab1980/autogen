import React from "react";

const codeToRunOnClient = `(function() {
  try {
    var mode = localStorage.getItem('darkmode');
    var supportDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches === true;
    if (!mode && supportDarkMode) document.getElementsByTagName("html")[0].className = 'dark';
    if (mode === 'dark') document.getElementsByTagName("html")[0].className = 'dark';
  } catch (e) {}
})();`;

export const onRenderBody = ({ setHeadComponents }) =>
  setHeadComponents([
    <script
      key="myscript"
      dangerouslySetInnerHTML={{ __html: codeToRunOnClient }}
    />,
  ]);

export { wrapRootElement } from "./gatsby-browser";
