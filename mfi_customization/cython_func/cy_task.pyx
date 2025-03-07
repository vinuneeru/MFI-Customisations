import frappe

def cy_mr_all(object doc,list mr_all,list l):
    for d in range(len(mr_all) - 1):
        if (
            mr_all[d]["total"] != "0"
            and mr_all[d]["total"] is not None
            and mr_all[d + 1]["total"] is not None
            ):
            if (
                    len(mr_all) > 0
                    and mr_all[d]["total"] != l[0]
                    and int(mr_all[d]["total"]) > 0
                    and doc.type_of_call == "Toner"
                ):
                doc.append(
                        "last_readings",
                        {
                            "date": mr_all[d]["reading_date"],
                            "type": mr_all[d]["machine_type"],
                            "asset": mr_all[d]["asset"],
                            "reading": mr_all[d]["black_and_white_reading"],
                            "reading_2": mr_all[d]["colour_reading"],
                            "total": (
                                int(mr_all[d]["black_and_white_reading"] or 0)
                                + int(mr_all[d]["colour_reading"] or 0)
                            ),
                            "yeild": int(mr_all[d]["total"])
                            - int(mr_all[d + 1]["total"])
                            or 0,
                            "actual_coverage": str(
                                round(
                                    5000
                                    / (
                                        int(mr_all[d]["total"])
                                        - int(mr_all[d + 1]["total"])
                                    )
                                    * 5,
                                    2,
                                )
                            )
                            + "%",
                            "rated_yield": 5000,
                        },
                    )

            else:
                doc.append(
                        "last_readings",
                        {
                            "date": mr_all[d]["reading_date"],
                            "type": mr_all[d]["machine_type"],
                            "asset": mr_all[d]["asset"],
                            "reading": mr_all[d]["black_and_white_reading"],
                            "reading_2": mr_all[d]["colour_reading"],
                            "total": (
                                int(mr_all[d]["black_and_white_reading"] or 0)
                                + int(mr_all[d]["colour_reading"] or 0)
                            ),
                            "yeild": 0,
                        },
                    )
