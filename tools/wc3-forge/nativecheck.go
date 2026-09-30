// nativecheck verifies the approved native-format compatibility round trip.
package main

import (
	"bytes"
	"fmt"
	"github.com/StephenSHorton/wc3-forge/internal/formats/doodadsdoo"
	"github.com/StephenSHorton/wc3-forge/internal/formats/unitsdoo"
	"github.com/StephenSHorton/wc3-forge/internal/formats/w3i"
	"os"
	"path/filepath"
)

func main() {
	dir := os.Args[1]
	for _, name := range []string{"war3map.w3i", "war3mapUnits.doo", "war3map.doo"} {
		raw, err := os.ReadFile(filepath.Join(dir, name))
		if err != nil {
			panic(err)
		}
		var out []byte
		switch name {
		case "war3map.w3i":
			var f *w3i.Info
			f, err = w3i.Parse(raw)
			if err == nil {
				out, err = w3i.Encode(f)
				fmt.Printf("metadata version=%d players=%d\n", f.FileVersion, len(f.Players))
			}
		case "war3mapUnits.doo":
			var f *unitsdoo.File
			f, err = unitsdoo.Parse(raw)
			if err == nil {
				out, err = unitsdoo.Encode(f)
				fmt.Printf("units version=%d count=%d\n", f.Version, len(f.Entities))
			}
		case "war3map.doo":
			var f *doodadsdoo.File
			f, err = doodadsdoo.Parse(raw)
			if err == nil {
				out, err = doodadsdoo.Encode(f)
				fmt.Printf("doodads version=%d count=%d\n", f.Version, len(f.Doodads))
			}
		}
		if err != nil {
			panic(fmt.Errorf("%s: %w", name, err))
		}
		if !bytes.Equal(raw, out) {
			panic(fmt.Errorf("%s: round trip differs (%d/%d bytes)", name, len(raw), len(out)))
		}
		fmt.Printf("%s: byte-identical round trip (%d bytes)\n", name, len(raw))
	}
}
