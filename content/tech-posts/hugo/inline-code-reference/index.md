+++
date = '2026-07-13T18:18:58+02:00'
draft = false
title = 'Dev: Adding inline reference to code file in Hugo'
+++

While writing a post, I wanted to include code from a separate file.

To do so, I had to add a shortcode to hugo to include the contents of another file within the same content folder.

I mostly followed the recommendation by jmooring [here](https://discourse.gohugo.io/t/how-to-include-code-snippet-from-a-file/54157/2), and you can see my implementation in this repository also at `layouts/_shortcodes/get-page-resource-content.html`

To ensure this works, make sure the post where you want to add the contents of another file respects the [page bundle format](https://gohugo.io/quick-reference/glossary/#page-bundle) and the file you want to add is within the page bundle's resources.

There are different types of resources in Hugo (global resources, page resources, remote resources; https://gohugo.io/quick-reference/glossary/#resource), and this shortcode currently supports page resources.

# Example

- Example with page bundle or local resource:
```python
{{% get-page-resource-content localPath="python_example.py" %}}
```

- Example with global asset under 'assets' folder:
```python
{{% get-page-resource-content globalPath="python_example_2.py" %}}
```


