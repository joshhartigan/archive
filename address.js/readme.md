# Address.js

## usage

Include the script, and put all the variables you need to access in an object
called `variables`.

When you want to access the value of a variable in HTML, use its **address** -
its name surrounded by `#{a_hash_and_braces}`.

## example

```html
<p>I have a #{colour} ball that is #{size}cm in diameter.</p>

<script src="address.min.js"></script>
<script>
  var variables = {
    colour: "orange",
    size: 234
  }
</script>
```

... will render as ...

I have a orange ball that is 234cm in diameter.

## notes

Include the address.js script at the **end** of your `<body>` tag, so that every
element is loaded when the script is run.

## author, license

Josh Hartigan, [MIT License](http://opensource.org/licenses/MIT)

