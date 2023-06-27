# substack-redirector

A simple app to extract meta-tags from a substack post and return a dummy response with meta tags embedded in it

## Setup

**Setup virtual environment**

```shell
python -m venv venv
source venv/bin/activate
```

**Install deps**

```shell
pip install -r requirements.txt
```

## Running

```shell
flask --app run.py run
```

## Example Usage

```shell
➜ curl http://localhost:5000/codeconfessions/code-confessions-digest-3
```

**Output**

```html
<!DOCTYPE html>
<html>
  <head>
    <title data-preact-helmet="">
      Code Confessions Digest: News, and Resources from Last Week
    </title>
    <meta charset="utf-8" />
    <meta
      content="24usqpep0ejc5w6hod3dulxwciwp0djs6c6ufp96av3t4whuxovj72wfkdjxu82yacb7430qjm8adbd5ezlt4592dq4zrvadcn9j9n-0btgdzpiojfzno16-fnsnu7xd"
      name="norton-safeweb-site-verification"
    />
    <meta
      content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0, viewport-fit=cover"
      name="viewport"
    />
    <meta content="Abhinav Upadhyay" name="author" />
    <meta
      content="https://codeconfessions.substack.com/p/code-confessions-digest-3"
      property="og:url"
    />
    <meta content="#ffffff" data-preact-helmet="" name="theme-color" />
    <meta content="article" data-preact-helmet="" property="og:type" />
    <meta
      content="Code Confessions Digest #3: News, and Resources from Last Week"
      data-preact-helmet=""
      property="og:title"
    />
    <meta
      content="Code Confessions Digest #3: News, and Resources from Last Week"
      data-preact-helmet=""
      name="twitter:title"
    />
    <meta
      content="Exploring CLI Tools, Debugging Techniques, Assembly Programming, Deep Learning, Compilers and More!"
      data-preact-helmet=""
      name="description"
    />
    <meta
      content="Exploring CLI Tools, Debugging Techniques, Assembly Programming, Deep Learning, Compilers and More!"
      data-preact-helmet=""
      property="og:description"
    />
    <meta
      content="Exploring CLI Tools, Debugging Techniques, Assembly Programming, Deep Learning, Compilers and More!"
      data-preact-helmet=""
      name="twitter:description"
    />
    <meta
      content="https://substackcdn.com/image/fetch/w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f6c8986-bb7e-4cac-b71e-debb62a7c07d_1080x1080.png"
      data-preact-helmet=""
      property="og:image"
    />
    <meta
      content="https://substackcdn.com/image/fetch/w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f6c8986-bb7e-4cac-b71e-debb62a7c07d_1080x1080.png"
      data-preact-helmet=""
      name="twitter:image"
    />
    <meta
      content="summary_large_image"
      data-preact-helmet=""
      name="twitter:card"
    />
  </head>
  <body></body>
</html>
⏎
```
