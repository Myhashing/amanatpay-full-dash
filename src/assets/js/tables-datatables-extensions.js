/**
 * DataTables Extensions (jquery)
 */

'use strict';

$(function () {
  var dt_scrollable_table = $('.dt-scrollableTable'),
    dt_fixedheader_table = $('.dt-fixedheader'),
    dt_fixedcolumns_table = $('.dt-fixedcolumns'),
    dt_select_table = $('.dt-select-table');

  // Scrollable
  // --------------------------------------------------------------------

  if (dt_scrollable_table.length) {
    var dt_scrollableTable = dt_scrollable_table.DataTable({
      language: {
        url: assetsPath + 'json/i18n/datatables-bs5/fa.json',
      },
      ajax: assetsPath + 'json/table-datatable.json',
      columns: [
        { data: 'full_name' },
        { data: 'post' },
        { data: 'email' },
        { data: 'city' },
        { data: 'start_date' },
        { data: 'salary' },
        { data: 'age' },
        { data: 'experience' },
        { data: '' },
        { data: '' }
      ],
      columnDefs: [
        {
          // Label
          targets: -2,
          render: function (data, type, full, meta) {
            var $status_number = full['status'];
            var $status = {
              1: { title: 'استعفاداده', class: 'bg-label-primary' },
              2: { title: 'حرفه‌ای', class: ' bg-label-success' },
              3: { title: 'ردشده', class: ' bg-label-danger' },
              4: { title: 'درحال بررسی', class: ' bg-label-warning' },
              5: { title: 'تایید شده', class: ' bg-label-info' }
            };
            if (typeof $status[$status_number] === 'undefined') {
              return data;
            }
            return (
              '<span class="badge ' + $status[$status_number].class + '">' + $status[$status_number].title + '</span>'
            );
          }
        },
        {
          // Actions
          targets: -1,
          title: 'عملیات',
          searchable: false,
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<div class="d-inline-block">' +
              '<a href="javascript:;" class="btn btn-sm btn-icon dropdown-toggle hide-arrow" data-bs-toggle="dropdown"><i class="text-primary ti ti-dots-vertical"></i></a>' +
              '<div class="dropdown-menu dropdown-menu-end m-0">' +
              '<a href="javascript:;" class="dropdown-item">جزئیات</a>' +
              '<a href="javascript:;" class="dropdown-item">بایگانی</a>' +
              '<div class="dropdown-divider"></div>' +
              '<a href="javascript:;" class="dropdown-item text-danger delete-record">حذف</a>' +
              '</div>' +
              '</div>' +
              '<a href="javascript:;" class="item-edit text-body"><i class="text-primary ti ti-pencil"></i></a>'
            );
          }
        }
      ],
      // Scroll options
      scrollY: '300px',
      scrollX: true,
      dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6 d-flex justify-content-center justify-content-md-end"f>>t<"row"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>'
    });
  }

  // FixedHeader
  // --------------------------------------------------------------------

  if (dt_fixedheader_table.length) {
    var dt_fixedheader = dt_fixedheader_table.DataTable({
      language: {
        url: assetsPath + 'json/i18n/datatables-bs5/fa.json',
      },
      ajax: assetsPath + 'json/table-datatable.json',
      columns: [
        { data: '' },
        { data: 'id' },
        { data: 'id' },
        { data: 'full_name' },
        { data: 'email' },
        { data: 'start_date' },
        { data: 'salary' },
        { data: 'status' },
        { data: '' }
      ],
      columnDefs: [
        {
          className: 'control',
          orderable: false,
          targets: 0,
          responsivePriority: 3,
          render: function (data, type, full, meta) {
            return '';
          }
        },
        {
          // For Checkboxes
          targets: 1,
          orderable: false,
          render: function () {
            return '<input type="checkbox" class="dt-checkboxes form-check-input">';
          },
          checkboxes: {
            selectAllRender: '<input type="checkbox" class="form-check-input">'
          },
          responsivePriority: 4
        },
        {
          targets: 2,
          visible: false
        },
        {
          // Avatar image/badge, Name and post
          targets: 3,
          render: function (data, type, full, meta) {
            var $user_img = full['avatar'],
              $name = full['full_name'],
              $post = full['post'];
            if ($user_img) {
              // For Avatar image
              var $output =
                '<img src="' + assetsPath + 'img/avatars/' + $user_img + '" alt="Avatar" class="rounded-circle">';
            } else {
              // For Avatar badge
              var stateNum = Math.floor(Math.random() * 6);
              var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
              var $state = states[stateNum],
                  $name = full['full_name'];
              let nameParts = $name.split(" ");
              let $initials = nameParts[0].charAt(0) + "‌" + nameParts[1].charAt(0);
              $output = '<span class="avatar-initial rounded-circle bg-label-' + $state + '">' + $initials + '</span>';
            }
            // Creates full output for row
            var $row_output =
              '<div class="d-flex justify-content-start align-items-center">' +
              '<div class="avatar-wrapper">' +
              '<div class="avatar me-2">' +
              $output +
              '</div>' +
              '</div>' +
              '<div class="d-flex flex-column ms-2">' +
              '<span class="emp_name text-truncate">' +
              $name +
              '</span>' +
              '<small class="emp_post text-truncate text-muted">' +
              $post +
              '</small>' +
              '</div>' +
              '</div>';
            return $row_output;
          },
          responsivePriority: 5
        },
        {
          responsivePriority: 1,
          targets: 4
        },
        {
          responsivePriority: 2,
          targets: 6
        },

        {
          // Label
          targets: -2,
          render: function (data, type, full, meta) {
            // var $rand_num = Math.floor(Math.random() * 5) + 1;
            var $status_number = full['status'];
            var $status = {
              1: { title: 'استعفاداده', class: 'bg-label-primary' },
              2: { title: 'حرفه‌ای', class: ' bg-label-success' },
              3: { title: 'ردشده', class: ' bg-label-danger' },
              4: { title: 'درحال بررسی', class: ' bg-label-warning' },
              5: { title: 'تایید شده', class: ' bg-label-info' }
            };
            if (typeof $status[$status_number] === 'undefined') {
              return data;
            }
            return (
              '<span class="badge ' + $status[$status_number].class + '">' + $status[$status_number].title + '</span>'
            );
          }
        },
        {
          // Actions
          targets: -1,
          title: 'عملیات',
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<div class="d-inline-block">' +
              '<a href="javascript:;" class="btn btn-sm btn-icon dropdown-toggle hide-arrow" data-bs-toggle="dropdown"><i class="text-primary ti ti-dots-vertical"></i></a>' +
              '<div class="dropdown-menu dropdown-menu-end m-0">' +
              '<a href="javascript:;" class="dropdown-item">جزئیات</a>' +
              '<a href="javascript:;" class="dropdown-item">بایگانی</a>' +
              '<div class="dropdown-divider"></div>' +
              '<a href="javascript:;" class="dropdown-item text-danger delete-record">حذف</a>' +
              '</div>' +
              '</div>' +
              '<a href="javascript:;" class="btn btn-sm btn-icon item-edit"><i class="text-primary ti ti-pencil"></i></a>'
            );
          }
        }
      ],
      order: [[2, 'desc']],
      dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6 d-flex justify-content-center justify-content-md-end"f>>t<"row"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>',
      displayLength: 7,
      lengthMenu: [7, 10, 25, 50, 75, 100],
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function (row) {
              var data = row.data();
              return 'جزئیات ' + data['full_name'];
            }
          }),
          type: 'column',
          renderer: function (api, rowIdx, columns) {
            var data = $.map(columns, function (col, i) {
              return col.title !== '' // ? Do not show row in modal popup if title is blank (for check box)
                ? '<tr data-dt-row="' +
                    col.rowIndex +
                    '" data-dt-column="' +
                    col.columnIndex +
                    '">' +
                    '<td>' +
                    col.title +
                    ':' +
                    '</td> ' +
                    '<td>' +
                    col.data +
                    '</td>' +
                    '</tr>'
                : '';
            }).join('');

            return data ? $('<table class="table"/><tbody />').append(data) : false;
          }
        }
      }
    });
    // Fixed header
    if (window.Helpers.isNavbarFixed()) {
      var navHeight = $('#layout-navbar').outerHeight();
      new $.fn.dataTable.FixedHeader(dt_fixedheader).headerOffset(navHeight);
    } else {
      new $.fn.dataTable.FixedHeader(dt_fixedheader);
    }
  }

  // FixedColumns
  // --------------------------------------------------------------------

  if (dt_fixedcolumns_table.length) {
    var dt_fixedcolumns = dt_fixedcolumns_table.DataTable({
      language: {
        url: assetsPath + 'json/i18n/datatables-bs5/fa.json',
      },
      ajax: assetsPath + 'json/table-datatable.json',
      columns: [
        { data: 'full_name' },
        { data: 'post' },
        { data: 'email' },
        { data: 'city' },
        { data: 'start_date' },
        { data: 'salary' },
        { data: 'age' },
        { data: 'experience' },
        { data: 'status' },
        { data: 'id' }
      ],
      columnDefs: [
        {
          // Label
          targets: -2,
          render: function (data, type, full, meta) {
            var $status_number = full['status'];
            var $status = {
              1: { title: 'استعفاداده', class: 'bg-label-primary' },
              2: { title: 'حرفه‌ای', class: ' bg-label-success' },
              3: { title: 'ردشده', class: ' bg-label-danger' },
              4: { title: 'درحال بررسی', class: ' bg-label-warning' },
              5: { title: 'تایید شده', class: ' bg-label-info' }
            };
            if (typeof $status[$status_number] === 'undefined') {
              return data;
            }
            return (
              '<span class="badge ' + $status[$status_number].class + '">' + $status[$status_number].title + '</span>'
            );
          }
        },
        {
          // Actions
          targets: -1,
          title: 'عملیات',
          searchable: false,
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<div class="d-inline-block">' +
              '<a href="javascript:;" class="btn btn-sm btn-icon dropdown-toggle hide-arrow" data-bs-toggle="dropdown"><i class="text-primary ti ti-dots-vertical"></i></a>' +
              '<div class="dropdown-menu dropdown-menu-end m-0">' +
              '<a href="javascript:;" class="dropdown-item">جزئیات</a>' +
              '<a href="javascript:;" class="dropdown-item">بایگانی</a>' +
              '<div class="dropdown-divider"></div>' +
              '<a href="javascript:;" class="dropdown-item text-danger delete-record"></i>حذف</a>' +
              '</div>' +
              '</div>' +
              '<a href="javascript:;" class="item-edit text-body"><i class="text-primary ti ti-pencil"></i></a>'
            );
          }
        }
      ],
      dom: '<"d-flex justify-content-between align-items-center row"<"col-sm-12 col-md-2 d-flex"f><"col-sm-12 col-md-10 d-none"i>>t',
      scrollY: 300,
      scrollX: true,
      scrollCollapse: true,
      paging: false,
      info: false,
      // Fixed column option
      fixedColumns: true
    });
  }

  // Select
  // --------------------------------------------------------------------

  if (dt_select_table.length) {
    var dt_select = dt_select_table.DataTable({
      language: {
        url: assetsPath + 'json/i18n/datatables-bs5/fa.json',
      },
      ajax: assetsPath + 'json/table-datatable.json',
      columns: [
        { data: 'id' },
        { data: 'full_name' },
        { data: 'post' },
        { data: 'email' },
        { data: 'city' },
        { data: 'start_date' },
        { data: 'salary' },
        { data: 'status' }
      ],
      columnDefs: [
        {
          // For Checkboxes
          targets: 0,
          searchable: false,
          orderable: false,
          render: function () {
            return '<input type="checkbox" class="dt-checkboxes form-check-input">';
          },
          checkboxes: {
            selectRow: true,
            selectAllRender: '<input type="checkbox" class="form-check-input">'
          }
        },
        {
          // Label
          targets: -1,
          render: function (data, type, full, meta) {
            var $status_number = full['status'];
            var $status = {
              1: { title: 'استعفاداده', class: 'bg-label-primary' },
              2: { title: 'حرفه‌ای', class: ' bg-label-success' },
              3: { title: 'ردشده', class: ' bg-label-danger' },
              4: { title: 'درحال بررسی', class: ' bg-label-warning' },
              5: { title: 'تایید شده', class: ' bg-label-info' }
            };
            if (typeof $status[$status_number] === 'undefined') {
              return data;
            }
            return (
              '<span class="badge ' + $status[$status_number].class + '">' + $status[$status_number].title + '</span>'
            );
          }
        }
      ],
      order: [[1, 'desc']],
      dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6 d-flex justify-content-center justify-content-md-end"f>><"table-responsive"t><"row"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>',
      select: {
        // Select style
        style: 'multi'
      }
    });
  }

  // Filter form control to default size
  // ? setTimeout used for multilingual table initialization
  setTimeout(() => {
    $('.dataTables_filter .form-control').removeClass('form-control-sm');
    $('.dataTables_length .form-select').removeClass('form-select-sm');
  }, 200);
});