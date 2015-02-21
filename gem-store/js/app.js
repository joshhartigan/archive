(function() {

  var appDependencies = [];
  var app = angular.module( 'store', appDependencies );

  app.controller( 'StoreController', function() {
    this.products = gems;
  });


  $(document).ready(function () {
    var trolley = 0; // number of items in trolley

    $( '.trolley-add' ).click( function() {
      trolley += 1;
      $( '.trolley' ).text( trolley );
    });

  });

  var gems = [
    {
      name: 'Colorgem',
      price: 5.80,
      description: 'This gem is older than anyone you\'ve ever met.',
      canPurchase: true,
      color: '#fbcd36'
    },
    {
      name: 'Rubygem',
      price: 2.95,
      description: 'Probably the nicest looking thing in the world.',
      canPurchase: true,
      color: '#e22607'
    },
    {
      name: 'Inigem',
      price: 0.99,
      description: 'A run-of-the-mill, common-garden gem. Nothing special.',
      canPurchase: true,
      color: '#124783'
    }
  ];

})();

