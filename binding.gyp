{
  "includes": [ "deps/common-sqlite.gypi" ],
  "variables": {
      "sqlite%":"internal",
      "sqlite_libname%":"sqlite3"
  },
  "targets": [
    {
      "target_name": "vscode-sqlite3",
      "xcode_settings": {
        "CLANG_CXX_LIBRARY": "libc++",
        # Target depends on
        # https://chromium.googlesource.com/chromium/src/+/master/build/config/mac/mac_sdk.gni#22
        "MACOSX_DEPLOYMENT_TARGET": "10.11",
      },
      "dependencies": [
        "<!(node -p \"require('node-addon-api').targets\"):node_addon_api_except"
      ],
      "msvs_configuration_attributes": {
        "SpectreMitigation": "Spectre"
      },
      "msvs_settings": {
        "VCCLCompilerTool": {
          "AdditionalOptions": [
            "/guard:cf",
            "/w34244",
            "/we4267",
            "/ZH:SHA_256"
          ]
        },
        "VCLinkerTool": {
          "AdditionalOptions": [
            "/guard:cf"
          ]
        }
      },
      "include_dirs": [
        "<!@(node -p \"require('node-addon-api').include\")"],
      "conditions": [
        ["sqlite != 'internal'", {
            "include_dirs": [
              "<!@(node -p \"require('node-addon-api').include\")", "<(sqlite)/include" ],
            "libraries": [
               "-l<(sqlite_libname)"
            ],
            "conditions": [ [ "OS=='linux'", {"libraries+":["-Wl,-rpath=<@(sqlite)/lib"]} ] ],
            "conditions": [ [ "OS!='win'", {"libraries+":["-L<@(sqlite)/lib"]} ] ],
            'msvs_settings': {
              'VCLinkerTool': {
                'AdditionalLibraryDirectories': [
                  '<(sqlite)/lib'
                ],
              },
            }
        },
        {
            "dependencies": [
              "<!(node -p \"require('node-addon-api').gyp\")",
              "deps/sqlite3.gyp:sqlite3"
            ]
        }
        ]
      ],
      "sources": [
        "src/backup.cc",
        "src/database.cc",
        "src/node_sqlite3.cc",
        "src/statement.cc"
      ],
      "defines": [ "NODE_API_SWALLOW_UNTHROWABLE_EXCEPTIONS" ]
    },
    #{
    #  "target_name": "action_after_build",
    #  "type": "none",
    #  "dependencies": [ "<(module_name)" ],
    #  "copies": [
    #      {
    #        "files": [ "<(PRODUCT_DIR)/<(module_name).node" ],
    #        "destination": "<(module_path)"
    #      }
    #  ]
    #}
  ]
}
