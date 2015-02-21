elements = document.body.getElementsByTagName('*');

function AddressJS(variables) {
  for ( var e = 0; e < elements.length; e++ ) {
    var current = elements[e];
    var content = current.textContent;

    for ( var c = 0; c < content.length; c++ ) {
      var address = '';

      if ( content[c] === '#' && content[c + 1] === '{' ) {
        accessorIndex = 1;
        charInAccessor = content[ c + accessorIndex ];

        while ( content[ c + accessorIndex + 1 ] !== '}' ) {
          accessorIndex++
          charInAccessor = content[ c + accessorIndex ];
          address += charInAccessor;
        }

        addressRegex = /#{.+}/
        var newContent = content.replace( addressRegex, variables[address] );
        current.innerText = newContent;

      }
    } // for ( var c = 0; c < content.length; c++ )

  } // for ( var e = 0; e < elements.length; e++ )
} // function AddressJS(variables)

