# Hi, I'm {{NAME}} 👋

{{ONE_LINE_TAGLINE}}

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/{{LINKEDIN}}/)
[![Email](https://img.shields.io/badge/-Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:{{EMAIL}})

{{SHORT_INTRO}}

### 📝 Latest blog posts
<!-- BLOG-POST-LIST:START -->
<!-- the workflow rewrites everything between these two markers; leave them exactly as-is -->
<!-- BLOG-POST-LIST:END -->

➡️ [More posts]({{BLOG_URL}})

### 📊 This week I coded
<!--START_SECTION:waka-->
<!--END_SECTION:waka-->

<p align="center">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username={{USERNAME}}&show_icons=true&hide_border=true&theme={{THEME}}" alt="{{NAME}}'s GitHub stats" />
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username={{USERNAME}}&layout=compact&hide_border=true&theme={{THEME}}" alt="Top languages" />
</p>

---
<p align="center">
  <a href="https://github.com/{{USERNAME}}/{{USERNAME}}/actions"><img src="https://github.com/{{USERNAME}}/{{USERNAME}}/workflows/Build%20README/badge.svg" alt="Build README"></a>
  &nbsp;•&nbsp; <i>This README updates itself every few hours.</i>
</p>

<!--
SETUP:
1. Put self-updating-workflow.yml in .github/workflows/
2. Set the WAKATIME_API_KEY secret (Settings → Secrets and variables → Actions) if using the waka block.
3. Replace {{BLOG_URL}} / the feed_list in the workflow with YOUR feed. Scrub any example feed.
4. Cron disables after 60 days of repo inactivity — no keepalive hacks (ToS).
-->
